from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import JSONResponse
from app.services.file_upload import handle_file_upload
from app.services.metadata_extraction import extract_metadata
import uuid
import httpx
from contextlib import asynccontextmanager
import asyncio
import threading
from app.services.orchestrator import start_saga, handle_document_uploaded_event
from app.services.message_queue import listen_for_events
 


app = FastAPI()

SAGA_ORCHESTRATOR_URL: str = "http://saga-orchestrator:5002"
def run_event_listener():
    """Run the event listener in a separate thread"""
    listen_for_events("document_uploaded", handle_document_uploaded_event)
    
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start event listener in background thread
    listener_thread = threading.Thread(target=run_event_listener, daemon=True)
    listener_thread.start()
    print("Event listener started")
    yield
    # Shutdown: Clean up if needed
    print("Shutting down")

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "ingestion-service"}
    )


@app.post("/upload")
async def upload_file(
    file: UploadFile = File(...),
    user_id: str = "user-uuid",
    file_type: str = "PDF",
    document_type: str = "Technical",
) -> JSONResponse:
    try:
        # Step 1: Handle file upload
        file_path = handle_file_upload(file)

        # Step 2: Extract metadata
        document_metadata = extract_metadata(file_path, uuid.UUID(user_id), file_type, document_type)

        # Step 3: Start the saga
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{SAGA_ORCHESTRATOR_URL}/start-saga",
                json={"document": document_metadata},
            )
            if response.status_code != 200:
                raise Exception(f"Failed to start saga: {response.text}")

        return JSONResponse(
            status_code=200,
            content={"message": "File upload process started successfully"},
        )
    except Exception as e:
        # Log specific errors for debugging
        print(f"An error occurred during upload: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")
