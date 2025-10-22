from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from app.services.minio_storage import (
    upload_file_to_minio, 
    delete_file_from_minio, 
    generate_object_path,
    get_file_metadata
)
from app.services.rabbitmq_utils import send_document_upload_message
import datetime
import tempfile
import os

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3001", "http://localhost:3000"],  # Allow upload-ui and other local dev ports
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancing"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "storage-service",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )

@app.post("/upload-document")
async def upload_document(
    file: UploadFile = File(...),
    brand: str = Form(...),
    business: str = Form(...),
    unit: str = Form(...),
    doc_type: str = Form(...),
    doc_name: str = Form(...),
    doc_date: str = Form(...),
    revision: str = Form(...),
    owner_team: str = Form(...),
    bucket_name: str = Form(default="documents")
):
    """
    Upload a document to MinIO with metadata and send RabbitMQ message
    
    Args:
        file: The document file to upload
        brand: Brand name (e.g., "acme")
        business: Business name (e.g., "retail")
        unit: Business unit (e.g., "supply-chain")
        doc_type: Document type (e.g., "spec")
        doc_name: Document name (e.g., "inventory-api")
        doc_date: Document date (e.g., "2025-01-15")
        revision: Revision number (e.g., "3")
        owner_team: Owner team (e.g., "platform")
        bucket_name: MinIO bucket name (default: "documents")
    """
    upload_time = datetime.datetime.now()
    temp_file_path = None
    
    try:
        # Validate required fields
        if not all([brand, business, unit, doc_type, doc_name, doc_date, revision, owner_team]):
            raise HTTPException(status_code=400, detail="All metadata fields are required")
        
        # Get file extension
        file_extension = file.filename.split('.')[-1] if '.' in file.filename else ''
        
        # Generate object path
        object_path = generate_object_path(
            brand=brand,
            business_unit=f"{business}/{unit}",
            document_name=doc_name,
            revision=revision,
            file_extension=file_extension
        )
        
        # Save uploaded file to temporary location
        with tempfile.NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            content = await file.read()
            temp_file.write(content)
            temp_file_path = temp_file.name
        
        # Prepare metadata
        document_metadata = {
            "brand": brand,
            "business": business,
            "unit": unit,
            "doc_type": doc_type,
            "doc_name": doc_name,
            "doc_date": doc_date,
            "revision": revision,
            "owner_team": owner_team,
            "original_filename": file.filename,
            "file_size": len(content),
            "content_type": file.content_type,
            "upload_timestamp": upload_time.isoformat()
        }
        
        # Upload to MinIO
        minio_url = upload_file_to_minio(
            file_path=temp_file_path,
            bucket_name=bucket_name,
            object_name=object_path,
            metadata=document_metadata
        )
        
        # Send RabbitMQ message
        send_document_upload_message(
            document_metadata=document_metadata,
            file_path=object_path,
            upload_time=upload_time
        )
        
        return JSONResponse(
            status_code=200,
            content={
                "message": "Document uploaded successfully",
                "minio_url": minio_url,
                "object_path": object_path,
                "metadata": document_metadata
            }
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        # Clean up temporary file
        if temp_file_path and os.path.exists(temp_file_path):
            os.unlink(temp_file_path)

@app.delete("/delete-document")
async def delete_document(bucket_name: str, object_path: str):
    """
    Delete a document from MinIO
    
    Args:
        bucket_name: MinIO bucket name
        object_path: Object path in MinIO
    """
    try:
        delete_file_from_minio(bucket_name, object_path)
        return JSONResponse(
            status_code=200,
            content={"message": "Document deleted successfully"}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
