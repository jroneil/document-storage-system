```
ingestion-service/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── models/
│   │   └── document.py
│   ├── services/
│   │   ├── file_upload.py
│   │   ├── metadata_extraction.py
│   │   └── message_queue.py
│   ├── utils/
│   │   └── file_utils.py
│   └── tests/
│       └── test_ingestion.py
├── requirements.txt
└── Dockerfile
```
The **Ingestion Service** is designed to handle **file uploads** from users, and it can read and process a wide variety of file types. Based on your requirements and the system's goals, the Ingestion Service should be capable of handling the following file types:

---

### **Supported File Types**
1. **Documents**:
   - PDF (`.pdf`)
   - Word Documents (`.doc`, `.docx`)
   - Excel Spreadsheets (`.xls`, `.xlsx`)
   - PowerPoint Presentations (`.ppt`, `.pptx`)
   - Text Files (`.txt`)
   - HTML Files (`.html`)

2. **Images**:
   - JPEG (`.jpg`, `.jpeg`)
   - PNG (`.png`)
   - GIF (`.gif`)
   - TIFF (`.tiff`)

3. **Videos**:
   - MP4 (`.mp4`)
   - AVI (`.avi`)
   - MOV (`.mov`)

4. **Audio**:
   - MP3 (`.mp3`)
   - WAV (`.wav`)

5. **Archives**:
   - ZIP (`.zip`)
   - RAR (`.rar`)

6. **Other Formats**:
   - JSON (`.json`)
   - XML (`.xml`)
   - CSV (`.csv`)

---

### **How the Ingestion Service Handles Files**
The Ingestion Service reads the uploaded file and performs the following steps:

1. **File Upload**:
   - The user uploads a file via an HTTP request (e.g., using a `multipart/form-data` form).
   - The file is temporarily stored on the server or in memory for processing.

2. **File Type Detection**:
   - The service detects the file type based on the file extension or MIME type.
   - Example: A file with the extension `.pdf` is identified as a PDF document.

3. **Metadata Extraction**:
   - Basic metadata (e.g., file name, size, type) is extracted from the file.
   - For certain file types (e.g., PDFs, images), additional metadata may be extracted (e.g., author, creation date, resolution).

4. **File Storage**:
   - The file is stored in a designated storage system (e.g., AWS S3) with a dynamically generated path.
   - The storage path is included in the metadata.

5. **Metadata and File Processing**:
   - The extracted metadata is sent to the **Metadata Service** for further processing and storage.
   - The file may be processed further (e.g., text extraction from PDFs, thumbnail generation for images).

---

### **Example: Handling a PDF File**
Here’s how the Ingestion Service processes a PDF file:

1. **File Upload**:
   - The user uploads a PDF file (`example.pdf`) via the `/upload` endpoint.

2. **File Type Detection**:
   - The service detects the file type as `application/pdf` based on the MIME type.

3. **Metadata Extraction**:
   - The service extracts basic metadata:
     ```json
     {
       "file_name": "example.pdf",
       "file_size": 1024,
       "file_type": "PDF",
       "upload_date": "2023-10-26T12:34:56Z"
     }
     ```

4. **File Storage**:
   - The file is stored in S3 at the path `/documents/{document_id}/example.pdf`.

5. **Metadata and File Processing**:
   - The metadata is sent to the **Metadata Service**.
   - The file is processed to extract text content (if needed).

---

### **Code Example: Handling File Uploads**
Here’s how the Ingestion Service handles file uploads in code:

#### **File: `ingestion-service/app/main.py`**
```python
from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from services.file_upload import handle_file_upload
from services.metadata_extraction import extract_metadata
from services.message_queue import publish_event
import uuid
import httpx

app = FastAPI()

METADATA_SERVICE_URL = "http://metadata-service:5001"

@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = "user-uuid",
    file_type: str = "PDF",
    document_type: str = "Technical"
):
    try:
        # Step 1: Handle file upload
        file_path = handle_file_upload(file)

        # Step 2: Extract metadata
        document_metadata = extract_metadata(file_path, uuid.UUID(user_id), file_type, document_type)

        # Step 3: Save metadata to Metadata Service
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{METADATA_SERVICE_URL}/save-metadata",
                json={"document": document_metadata}
            )
            if response.status_code != 200:
                raise Exception(f"Failed to save metadata: {response.text}")

        # Step 4: Publish event: document_uploaded
        publish_event("document_uploaded", {"document": document_metadata})

        return JSONResponse(
            status_code=200,
            content={"message": "File uploaded successfully", "metadata": document_metadata}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

---

### **File Type Detection**
The Ingestion Service can detect file types using the `file.content_type` attribute (MIME type) or the file extension.

#### **Example: Detecting File Type**
```python
from fastapi import UploadFile

def detect_file_type(file: UploadFile) -> str:
    # Use MIME type or file extension
    if file.content_type == "application/pdf":
        return "PDF"
    elif file.filename.endswith(".docx"):
        return "Word"
    elif file.filename.endswith(".xlsx"):
        return "Excel"
    else:
        return "Unknown"
```

---

### **Handling Different File Types**
The Ingestion Service can handle different file types by using appropriate libraries:

1. **PDFs**:
   - Use `PyPDF2` or `pdfminer` to extract text and metadata.

2. **Images**:
   - Use `Pillow` to extract metadata (e.g., resolution) and generate thumbnails.

3. **Videos**:
   - Use `moviepy` or `ffmpeg` to extract metadata (e.g., duration, resolution).

4. **CSV/Excel**:
   - Use `pandas` to read and process the data.

---

### **Conclusion**
The **Ingestion Service** is designed to handle a wide variety of file types, including documents, images, videos, and more. It reads the uploaded file, extracts metadata, and processes the file based on its type. This flexibility ensures that the system can accommodate diverse user needs.

Let me know if you need further clarification or enhancements!
