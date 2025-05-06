# Azure Image Tagging System

This project demonstrates a simple cloud-native system using **Azure Storage** services:
- Azure Blob Storage
- Azure Queue Storage
- Azure Table Storage

The use-case:  
**"Users upload images via a frontend. Images are stored in Blob Storage. A background service asynchronously analyzes and tags the images. Tags are stored in Table Storage for fast retrieval."**

---

## 🧱 Architecture Overview

- **Frontend:** Uploads images via HTTP
- **Blob Storage:** Stores uploaded image files
- **Queue Storage:** Stores a reference message (e.g., blob URL + user ID)
- **Worker:** Reads messages, processes images, generates tags
- **Table Storage:** Saves tags per user/image for querying

![Architecture](https://github.com/user-attachments/assets/675d50e8-41a5-450b-822f-e620705306cb)
[Azure Image Tagging System Presentation](https://github.com/user-attachments/files/20062260/azure_image_tagging_system.pptx)

---

## 🧾 Azure Technology Summary

| Service             | Purpose                         | Strengths                             | Limitations                          |
|---------------------|----------------------------------|----------------------------------------|---------------------------------------|
| **Blob Storage**     | Unstructured data (e.g., images) | Highly durable, scalable, cheap tiers | No metadata querying                  |
| **Queue Storage**    | Async communication              | Simple decoupling, reliable delivery   | At-least-once, 64KB message limit     |
| **Table Storage**    | Structured NoSQL metadata        | Fast lookups, cheap NoSQL              | Limited query model, no joins         |

---

## 📁 Project Structure

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

---

## 📄 License

MIT License
