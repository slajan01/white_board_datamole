# Azure Human Detection System (Architecture Overview)

# SYSTEM OVERVIEW:
# - User uploads image to web app
# - Image is stored in Azure Blob Storage
# - A message is placed into Azure Queue Storage
# - Worker reads queue, processes image, classifies it using an inline neural network
# - Classification results are stored in Azure Table Storage

# -- CODE STRUCTURE --
# 1. upload_image.py       --> simulate upload and queue message
# 2. worker.py             --> async human detection with inline neural network
# 3. utils.py              --> shared helpers for Azure Storage interaction
# 4. config.py             --> connection strings / settings
# 5. train_model.py        --> simple training script for neural network
# 6. README.md             --> project overview and instructions

# --------------------
# config.py
# --------------------
import os

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = "images"
QUEUE_NAME = "imageprocessingqueue"
TABLE_NAME = "imageclassifications"
USE_TRAINED_MODEL = os.getenv("USE_TRAINED_MODEL", "false").lower() == "true"

# --------------------
# utils.py
# --------------------
from azure.storage.blob import BlobServiceClient
from azure.storage.queue import QueueServiceClient
from azure.data.tables import TableServiceClient
from config import AZURE_STORAGE_CONNECTION_STRING

blob_service = BlobServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
queue_service = QueueServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)
table_service = TableServiceClient.from_connection_string(AZURE_STORAGE_CONNECTION_STRING)

def upload_to_blob(file_path, blob_name):
    blob_client = blob_service.get_blob_client(container=BLOB_CONTAINER_NAME, blob=blob_name)
    with open(file_path, "rb") as data:
        blob_client.upload_blob(data, overwrite=True)
    return blob_client.url

def enqueue_image(blob_url, user_id, image_id):
    queue_client = queue_service.get_queue_client(QUEUE_NAME)
    queue_client.send_message(f"{blob_url}|{user_id}|{image_id}")

def store_classification(user_id, image_id, is_human):
    table_client = table_service.get_table_client(table_name=TABLE_NAME)
    entity = {
        'PartitionKey': user_id,
        'RowKey': image_id,
        'is_human': str(is_human)
    }
    table_client.upsert_entity(entity)

# --------------------
# upload_image.py
# --------------------
import uuid
from utils import upload_to_blob, enqueue_image

def simulate_upload(file_path, user_id):
    image_id = str(uuid.uuid4())
    blob_url = upload_to_blob(file_path, image_id)
    enqueue_image(blob_url, user_id, image_id)
    print(f"Uploaded {file_path} to {blob_url} and enqueued processing task.")

# simulate_upload("sample.jpg", "user123")

# --------------------
# worker.py
# --------------------
from utils import store_classification
from config import QUEUE_NAME, USE_TRAINED_MODEL
from azure.storage.queue import QueueServiceClient

import numpy as np
import requests
from io import BytesIO
from PIL import Image
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense
from tensorflow.keras.preprocessing import image

queue_client = queue_service.get_queue_client(queue=QUEUE_NAME)

# Load trained model or create inline model
model = None
if USE_TRAINED_MODEL:
    model = load_model("trained_human_detection_model.h5")
else:
    model = Sequential([
        Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 3)),
        MaxPooling2D(pool_size=(2, 2)),
        Conv2D(32, (3, 3), activation='relu'),
        MaxPooling2D(pool_size=(2, 2)),
        Flatten(),
        Dense(64, activation='relu'),
        Dense(1, activation='sigmoid')
    ])
    model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])


def process_images():
    messages = queue_client.receive_messages(messages_per_page=5)
    for msg_batch in messages.by_page():
        for msg in msg_batch:
            try:
                blob_url, user_id, image_id = msg.content.split("|")
                print(f"Processing image {image_id} from {blob_url}")
                is_human = classify_image(blob_url)
                store_classification(user_id, image_id, is_human)
                queue_client.delete_message(msg)
                print(f"Stored classification for {image_id}: {'Human' if is_human else 'Not Human'}")
            except Exception as e:
                print(f"Failed to process message: {e}")


def classify_image(blob_url):
    try:
        response = requests.get(blob_url)
        img = Image.open(BytesIO(response.content)).convert('RGB')
        img = img.resize((224, 224))
        img_array = image.img_to_array(img) / 255.0
        img_array = np.expand_dims(img_array, axis=0)
        prediction = model.predict(img_array)[0][0]
        return prediction >= 0.5
    except Exception as err:
        print(f"Image classification failed: {err}")
        return False

# process_images()

# --------------------
# train_model.py
# --------------------
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense

# Paths to training data (adjust these paths to your local folders)
TRAIN_DIR = "./data/train"

# Prepare data generator
train_datagen = ImageDataGenerator(rescale=1./255)
train_generator = train_datagen.flow_from_directory(
    TRAIN_DIR,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# Build model
model = Sequential([
    Conv2D(16, (3, 3), activation='relu', input_shape=(224, 224, 3)),
    MaxPooling2D(2, 2),
    Conv2D(32, (3, 3), activation='relu'),
    MaxPooling2D(2, 2),
    Flatten(),
    Dense(64, activation='relu'),
    Dense(1, activation='sigmoid')
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])
model.fit(train_generator, epochs=5)
model.save("trained_human_detection_model.h5")
print("Model training complete and saved.")
