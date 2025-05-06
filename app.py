# Azure Image Upload and Tagging System (Architecture Overview)

# SYSTEM OVERVIEW:
# - User uploads image to web app
# - Image is stored in Azure Blob Storage
# - A message is placed into Azure Queue Storage
# - Worker reads queue, processes image, tags it
# - Tags are stored in Azure Table Storage

# -- CODE STRUCTURE --
# 1. upload_image.py       --> simulate upload and queue message
# 2. worker.py             --> simulate async tagging worker
# 3. utils.py              --> shared helpers for Azure Storage interaction
# 4. config.py             --> connection strings / settings

# --------------------
# config.py
# --------------------
import os

AZURE_STORAGE_CONNECTION_STRING = os.getenv("AZURE_STORAGE_CONNECTION_STRING")
BLOB_CONTAINER_NAME = "images"
QUEUE_NAME = "imageprocessingqueue"
TABLE_NAME = "imagetags"

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

def store_tags(user_id, image_id, tags):
    table_client = table_service.get_table_client(table_name=TABLE_NAME)
    entity = {
        'PartitionKey': user_id,
        'RowKey': image_id,
        'tags': ','.join(tags)
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
from utils import store_tags
from config import QUEUE_NAME
from azure.storage.queue import QueueServiceClient
import random

queue_client = queue_service.get_queue_client(queue=QUEUE_NAME)

def process_images():
    messages = queue_client.receive_messages(messages_per_page=5)
    for msg_batch in messages.by_page():
        for msg in msg_batch:
            try:
                blob_url, user_id, image_id = msg.content.split("|")
                print(f"Processing image {image_id} from {blob_url}")
                tags = simulate_image_tagging(blob_url)
                store_tags(user_id, image_id, tags)
                queue_client.delete_message(msg)
                print(f"Stored tags for {image_id}: {tags}")
            except Exception as e:
                print(f"Failed to process message: {e}")


def simulate_image_tagging(blob_url):
    # Simulate AI tagging
    tag_pool = ["dog", "cat", "tree", "person", "car", "flower"]
    return random.sample(tag_pool, k=2)

# process_images()
