# Azure Human Detection System

This project implements a scalable cloud-based system using Microsoft Azure services to detect whether an uploaded image contains a human using a neural network.

---

## 📦 System Overview

<<<<<<< HEAD
- **Frontend:** Uploads images via HTTP
- **Blob Storage:** Stores uploaded image files
- **Queue Storage:** Stores a reference message (e.g., blob URL + user ID)
- **Worker:** Reads messages, processes images, generates tags
- **Table Storage:** Saves tags per user/image for querying

![Architecture](https://github.com/user-attachments/assets/675d50e8-41a5-450b-822f-e620705306cb)
[Azure Image Tagging System Presentation](https://github.com/user-attachments/files/20062260/azure_image_tagging_system.pptx)
=======
1. Users upload images via a frontend or CLI.
2. Images are stored in **Azure Blob Storage**.
3. A message is placed into **Azure Queue Storage**.
4. A Python **worker service** retrieves the message, downloads the image, and classifies it using a CNN.
5. Classification results are stored in **Azure Table Storage**.


---

## ⚙️ Technology Stack

| Component        | Technology                 |
|------------------|-----------------------------|
| Image Storage    | Azure Blob Storage          |
| Messaging Queue  | Azure Queue Storage         |
| Classification   | TensorFlow Keras CNN (inline or trained `.h5`) |
| Metadata Store   | Azure Table Storage         |
| Language         | Python                      |

---


## 📁 Project Structure
```
azure-image-tagging-system/
├── frontend/ # (Optional) Frontend mock
│ └── upload.py # Upload to Blob & Queue
├── worker/ # Background processor
│ └── tag_processor.py # Downloads blobs, generates tags
├── shared/ # Utilities or models
│ └── azure_helpers.py # Azure client wrappers
├── assets/
│ └── azure_image_tagging_architecture.png
├── azure_image_tagging_system.pptx
└── README.md
```
---

## 🚀 Getting Started

1. Create Azure Storage Account with Blob, Table, and Queue enabled.
2. Configure connection string in `azure_helpers.py`.
3. Run `upload.py` to simulate image uploads.
4. Run `tag_processor.py` to process images asynchronously.

---

## 🧠 Notes

- Tags are mock-generated; integrate your ML model easily.
- Extend with Azure Functions, Logic Apps, or Event Grid for automation.
- Make sure to secure access with SAS or RBAC in production.
=======
## 🧠 Neural Network Modes

- **Default (Inline)**: Untrained CNN created at runtime.
- **Trained Model**: Use your `.h5` model by setting:

```bash
export USE_TRAINED_MODEL=true
```

And ensure `trained_human_detection_model.h5` exists in the project root.

---

## 🧪 Training Your Model

1. Organize your dataset:
```
./data/train/
    ├── human/
    └── not_human/
```

2. Run the training script:
```bash
python train_model.py
```

3. It will generate `trained_human_detection_model.h5`.

---

## 🚀 How to Run

1. Set your Azure Storage connection string:
```bash
export AZURE_STORAGE_CONNECTION_STRING="<your_connection_string>"
```

2. Upload an image:
```bash
python upload_image.py
```

3. Process messages and classify images:
```bash
python worker.py
```

---

## 📂 Project Structure

```
azure-human-detection/
├── config.py
├── utils.py
├── upload_image.py
├── worker.py
├── train_model.py
└── trained_human_detection_model.h5  # optional
```

---

## ✅ Features

- Fully functional offline image classification pipeline
- Inline model creation for structure prototyping
- Easy switch to trained model via env var
- Modular design using Azure SDK


---

## 📄 License


MIT License
=======
MIT License
>>>>>>> 49c2a49 (Final touch)
