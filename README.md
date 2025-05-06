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

![Architecture](azure_image_tagging_architecture.png)

---

## 🧾 Azure Technology Summary

| Service             | Purpose                         | Strengths                             | Limitations                          |
|---------------------|----------------------------------|----------------------------------------|---------------------------------------|
| **Blob Storage**     | Unstructured data (e.g., images) | Highly durable, scalable, cheap tiers | No metadata querying                  |
| **Queue Storage**    | Async communication              | Simple decoupling, reliable delivery   | At-least-once, 64KB message limit     |
| **Table Storage**    | Structured NoSQL metadata        | Fast lookups, cheap NoSQL              | Limited query model, no joins         |

---


