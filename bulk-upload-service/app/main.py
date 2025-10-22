from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.services.file_upload import handle_file_upload
from app.services.metadata_parser import MetadataParser
from app.services.message_queue import publish_bulk_upload_message
import datetime
import uuid
import logging

# Configure logging
logger = logging.getLogger(__name__)
app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3002"],
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
        # Validate file type
        allowed_extensions = ['csv', 'json', 'xml', 'xlsx', 'xls']
        file_extension = file.filename.lower().split('.')[-1]
        
        if file_extension not in allowed_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Unsupported file type: {file_extension}. Allowed types: {', '.join(allowed_extensions)}"
            )

        # Step 1: Handle file upload
        file_path = handle_file_upload(file)

        # Step 2: Parse metadata from the file using enhanced parser
        parser = MetadataParser()
        job_id = str(uuid.uuid4())
        batch_result = parser.parse_file(file_path, job_id)

        # Step 3: Send batch message to the message queue
        publish_bulk_upload_message(batch_result)

        # Return job information
        return JSONResponse(
            status_code=200,
            content={
                "message": "Bulk upload processing started",
                "job_id": job_id,
                "records_processed": len(batch_result.get('records', [])),
                "validation_errors": len(batch_result.get('validation_errors', [])),
                "source_file": batch_result.get('source_file')
            }
        )
    except Exception as e:
        logger.error(f"Bulk upload failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    """Get job status and processing results"""
    # TODO: Implement job status tracking
    # For now, return a placeholder response
    return JSONResponse(
        status_code=200,
        content={
            "job_id": job_id,
            "status": "completed",  # Placeholder
            "message": "Job status tracking not yet implemented"
        }
    )
