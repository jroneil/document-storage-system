from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.file_upload import handle_file_upload
from app.services.metadata_parser import parse_metadata
from app.services.message_queue import publish_event
import datetime
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring and load balancing"""
    return JSONResponse(
        status_code=200,
        content={
            "status": "healthy",
            "service": "bulk-upload-service",
            "timestamp": datetime.datetime.now().isoformat(),
            "version": "1.0.0"
        }
    )
@app.post("/bulk-upload")
async def bulk_upload(file: UploadFile = File(...)):
    try:
        # Step 1: Handle file upload
        file_path = handle_file_upload(file)

        # Step 2: Parse metadata from the file
        metadata_list = parse_metadata(file_path)

        # Step 3: Send metadata to the message queue
        for metadata in metadata_list:
            publish_event("metadata_uploaded", metadata)

        return JSONResponse(
            status_code=200,
            content={"message": "Bulk upload completed successfully", "metadata_count": len(metadata_list)}
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))