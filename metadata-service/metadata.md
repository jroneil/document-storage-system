Certainly! Below is a **Design Document** for your document storage service, incorporating all the requirements and metadata discussed. This document outlines the system architecture, data models, and key considerations.

---

# **Design Document: Document Storage Service**

## **1. Overview**
This document outlines the design of a document storage service that allows users to upload, organize, and retrieve documents with rich metadata. The service supports:
- Standard metadata (e.g., file type, document type, division, business unit).
- Optional metadata (e.g., branding, availability by country, languages).
- Flexible storage for variable-length or document-specific metadata.

---

## **2. System Architecture**
The system is composed of two main components:
1. **PostgreSQL**: For storing standard metadata and relational data.
2. **MongoDB**: For storing optional, variable-length, or document-specific metadata.

### **2.1 High-Level Architecture**
```
+-------------------+       +-------------------+       +-------------------+
|                   |       |                   |       |                   |
|   Client (UI/API) | <---> |   Backend Service | <---> |   PostgreSQL      |
|                   |       |                   |       |                   |
+-------------------+       +-------------------+       +-------------------+
                                                                   |
                                                                   v
                                                           +-------------------+
                                                           |   MongoDB         |
                                                           |                   |
                                                           +-------------------+
```

---

## **3. Data Models**

### **3.1 PostgreSQL Schema**
The PostgreSQL database stores standard metadata for all documents.

#### **Table: `documents`**
| Column Name           | Data Type               | Description                                                                 |
|-----------------------|-------------------------|-----------------------------------------------------------------------------|
| `document_id`         | `UUID`                  | Unique identifier for the document (primary key).                          |
| `file_name`           | `TEXT`                  | Name of the uploaded file.                                                 |
| `file_size`           | `BIGINT`                | Size of the file in bytes.                                                 |
| `file_type`           | `TEXT`                  | File format (e.g., PDF, HTML, Video, DOC, Excel).                          |
| `upload_date`         | `TIMESTAMP WITH TIME ZONE` | Timestamp when the file was uploaded.                                     |
| `last_modified_date`  | `TIMESTAMP WITH TIME ZONE` | Timestamp when the file was last modified.                                |
| `user_id`             | `UUID`                  | ID of the user who uploaded the file.                                      |
| `tags`                | `TEXT[]`                | Array of tags for easier searching.                                        |
| `description`         | `TEXT`                  | Optional description of the document.                                      |
| `storage_path`        | `TEXT`                  | Path or URL to the file in storage.                                        |
| `version`             | `INTEGER`               | Version number of the document (default: 1).                               |
| `checksum`            | `TEXT`                  | Hash of the file for integrity verification (e.g., MD5, SHA-256).          |
| `acl`                 | `JSONB`                 | Access control list (e.g., `{"read": ["user1"], "write": ["user1"]}`).     |
| `thumbnail_path`      | `TEXT`                  | Path to a thumbnail image (if applicable).                                 |
| `expiration_date`     | `TIMESTAMP WITH TIME ZONE` | Optional expiration date for the document.                               |
| `category`            | `TEXT`                  | Optional category or folder for grouping.                                  |
| `division`            | `TEXT`                  | Division associated with the document.                                     |
| `business_unit`       | `TEXT`                  | Business unit associated with the document.                                |
| `brand_id`            | `UUID`                  | Optional reference to a brand (if applicable).                             |
| `document_type`       | `TEXT`                  | Document type (e.g., Technical, User, Marketing).                          |

#### **Indexes**
- `idx_document_user`: Index on `user_id`.
- `idx_document_tags`: GIN index on `tags`.
- `idx_document_upload_date`: Index on `upload_date`.
- `idx_document_category`: Index on `category`.
- `idx_document_division`: Index on `division`.
- `idx_document_business_unit`: Index on `business_unit`.
- `idx_document_brand`: Index on `brand_id`.
- `idx_document_file_type`: Index on `file_type`.
- `idx_document_document_type`: Index on `document_type`.

---

### **3.2 MongoDB Schema**
MongoDB stores optional, variable-length, or document-specific metadata.

#### **Collection: `document_metadata`**
Each document in the collection corresponds to a document in PostgreSQL and contains optional metadata.

##### **Example Document**
```json
{
    "document_id": "uuid-from-postgresql",
    "available_countries": ["US", "CA", "GB"], // List of country codes (ISO 3166-1 alpha-2)
    "languages": ["en", "fr", "es"], // List of language codes (ISO 639-1)
    "brand_colors": ["#FF0000", "#00FF00"], // Brand-specific colors
    "brand_logo_path": "/path/to/logo.png", // Path to the brand logo
    "campaign_name": "Summer Sale 2023", // Campaign name (if applicable)
    "product_line": "Electronics" // Product line (if applicable)
}
```

---

## **4. Key Features**

### **4.1 Document Upload**
1. User uploads a file via the UI/API.
2. Backend service:
   - Generates a unique `document_id`.
   - Extracts standard metadata (e.g., `file_name`, `file_size`, `file_type`).
   - Stores standard metadata in PostgreSQL.
   - Stores optional metadata in MongoDB.

### **4.2 Document Retrieval**
1. User queries for documents using filters (e.g., `file_type`, `document_type`, `division`).
2. Backend service:
   - Queries PostgreSQL for standard metadata.
   - Queries MongoDB for optional metadata (if needed).

### **4.3 Document Versioning**
- Each document has a `version` field in PostgreSQL.
- When a new version is uploaded, the `version` is incremented, and the old version is archived.

### **4.4 Access Control**
- The `acl` field in PostgreSQL defines who can read or write the document.
- Access control is enforced at the API level.

---

## **5. Key Considerations**

### **5.1 Scalability**
- PostgreSQL is used for structured, frequently queried data.
- MongoDB is used for flexible, variable-length data to avoid schema bloat in PostgreSQL.

### **5.2 Query Performance**
- Indexes in PostgreSQL ensure fast queries for standard metadata.
- MongoDB’s flexible schema allows efficient storage and retrieval of optional metadata.

### **5.3 Data Integrity**
- The `checksum` field ensures file integrity.
- Relationships between PostgreSQL and MongoDB are maintained using `document_id`.

### **5.4 Localization**
- The `languages` field in MongoDB supports multi-language documents.
- Country-specific availability is managed via the `available_countries` field.

---

## **6. Future Enhancements**
1. **Search Functionality**: Integrate a search engine (e.g., Elasticsearch) for full-text search across documents.
2. **Analytics**: Add reporting and analytics to track document usage and trends.
3. **File Previews**: Generate previews for documents (e.g., PDF thumbnails, video previews).
4. **Advanced Access Control**: Implement role-based access control (RBAC) for finer-grained permissions.

---

## **7. Example Use Case**
### **Uploading a Document**
1. A user uploads a PDF file (`user_guide.pdf`) with the following metadata:
   - **Standard Metadata**:
     - `file_name`: `user_guide.pdf`
     - `file_type`: `application/pdf`
     - `document_type`: `User`
     - `division`: `Sales`
     - `business_unit`: `North America`
   - **Optional Metadata**:
     - `available_countries`: `["US", "CA"]`
     - `languages`: `["en", "es"]`
     - `brand_colors`: `["#FF0000", "#00FF00"]`
2. The backend service:
   - Stores standard metadata in PostgreSQL.
   - Stores optional metadata in MongoDB.

### **Querying for Documents**
1. A user queries for all `User` documents available in the `US`.
2. The backend service:
   - Queries PostgreSQL for documents with `document_type = 'User'`.
   - Queries MongoDB for documents with `available_countries` containing `US`.

---

This design document provides a comprehensive blueprint for your document storage service. Let me know if you need further refinements or additional details!