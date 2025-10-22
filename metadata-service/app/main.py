from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from contextlib import asynccontextmanager
import asyncio
import threading
import json
import logging
from app.services.message_queue import listen_for_events
from app.services.postgres_service import save_document_metadata
from app.models.document import DocumentMetadata
import uuid
from datetime import datetime

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def handle_metadata_uploaded_event(ch, method, properties, body):
    """Handle metadata_uploaded events from the message queue"""
    try:
        payload = json.loads(body)
        logger.info(f"Received metadata_uploaded event: {payload}")
        
        # Log detailed metadata information
        logger.info(f"Raw metadata from queue: {json.dumps(payload, indent=2, default=str)}")
        
        # Validate and transform the metadata
        document_metadata = transform_metadata(payload)
        
        # Log transformed metadata before saving
        logger.info(f"Transformed metadata ready for database: {json.dumps(document_metadata, indent=2, default=str)}")
        
        # Save to database
        save_document_metadata(document_metadata)
        
        logger.info(f"Successfully saved document metadata for document_id: {document_metadata['document_id']}")
        
    except Exception as e:
        logger.error(f"Failed to handle metadata_uploaded event: {str(e)}")
        logger.error(f"Failed payload: {body.decode() if body else 'No body'}")
        # Re-queue the message for retry
        ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

def transform_metadata(raw_metadata: dict) -> dict:
    """Transform raw metadata from message queue to database format"""
    try:
        # Extract metadata from the message structure
        # The storage service sends: {"event_type": "document_uploaded", "file_path": "...", "metadata": {...}}
        metadata = raw_metadata.get('metadata', {})
        file_path = raw_metadata.get('file_path', '')
        
        # Generate document_id if not provided
        document_id = metadata.get('document_id')
        if not document_id:
            document_id = str(uuid.uuid4())
        
        # Ensure document_id is properly formatted as UUID string
        try:
            # Try to parse as UUID to validate format
            uuid.UUID(document_id)
        except ValueError:
            # If invalid, generate a new UUID
            document_id = str(uuid.uuid4())
        
        # Get current timestamp for upload and modification dates
        current_time = datetime.now()
        
        # Transform the metadata to match the database schema
        transformed_metadata = {
            'document_id': document_id,
            'file_name': metadata.get('original_filename', ''),
            'file_size': metadata.get('file_size', 0),
            'file_type': metadata.get('content_type', ''),
            'upload_date': metadata.get('upload_timestamp', current_time),
            'last_modified_date': metadata.get('upload_timestamp', current_time),
            'user_id': metadata.get('user_id', str(uuid.uuid4())),  # Default user if not provided
            'tags': metadata.get('tags', []),
            'description': metadata.get('description', ''),
            'storage_path': file_path,
            'version': metadata.get('version', 1),
            'checksum': metadata.get('checksum', ''),
            'acl': metadata.get('acl', {}),
            'thumbnail_path': metadata.get('thumbnail_path', ''),
            'expiration_date': metadata.get('expiration_date'),
            'category': metadata.get('category'),
            'division': metadata.get('division'),
            'business_unit': metadata.get('business_unit'),
            'brand_id': metadata.get('brand_id'),
            'document_type': metadata.get('doc_type', 'Document')
        }
        
        return transformed_metadata
        
    except Exception as e:
        logger.error(f"Failed to transform metadata: {str(e)}")
        raise

def run_event_listener():
    """Run the event listener in a separate thread"""
    logger.info("Starting metadata event listener...")
    listen_for_events("document_upload_queue", handle_metadata_uploaded_event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start event listener in background thread
    listener_thread = threading.Thread(target=run_event_listener, daemon=True)
    listener_thread.start()
    logger.info("Metadata event listener started")
    yield
    # Shutdown: Clean up if needed
    logger.info("Shutting down metadata service")

app = FastAPI(lifespan=lifespan)

@app.get("/health")
async def health_check():
    """Health check endpoint for monitoring service status"""
    return JSONResponse(
        status_code=200,
        content={"status": "healthy", "service": "metadata-service"}
    )

# ... rest of your endpoints remain the same
