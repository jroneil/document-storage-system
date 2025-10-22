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
    job_id = 'unknown_job'
    source_file = 'unknown_file'
    try:
        payload = json.loads(body)
        job_id = payload.get('job_id', 'unknown_job')
        source_file = payload.get('source_file', 'unknown_file')
        logger.info(f"Received metadata_uploaded event for job {job_id}, source {source_file}")
        
        # Log detailed metadata information
        logger.debug(f"Raw metadata from queue: {json.dumps(payload, indent=2, default=str)}")
        
        # Determine if this is a batch message or a single record message
        if 'records' in payload and isinstance(payload['records'], list):
            # This is a batch message from bulk-upload-service
            records_to_transform = payload['records']
        else:
            # This is a single record message (e.g., from storage-service)
            records_to_transform = [payload]
            logger.debug(f"Interpreting message as a single record for job {job_id}.")

        # Transform the records (transform_metadata expects a dict with a 'records' key)
        # We create a temporary dict that matches the expected structure for transform_metadata
        temp_payload_for_transformation = {
            "job_id": job_id,
            "source_file": source_file,
            "source": payload.get('source', 'unknown'), # Preserve original source if available
            "idempotency_key": payload.get('idempotency_key'), # Preserve original idempotency_key
            "transaction_type": payload.get('transaction_type', 'new'), # Preserve original transaction_type
            "bucket": payload.get('bucket', 'documents'), # Preserve original bucket
            "records": records_to_transform
        }
        
        transformed_records = transform_metadata(temp_payload_for_transformation)
        
        if not transformed_records:
            logger.warning(f"No records to save for job {job_id}, source {source_file} after transformation.")
            ch.basic_ack(delivery_tag=method.delivery_tag)
            return

        # Log transformed metadata before saving
        logger.debug(f"Transformed {len(transformed_records)} records ready for database for job {job_id}.")
        
        # Save each record to the database
        for record in transformed_records:
            # Log transformed record before saving
            logger.debug(f"Saving record: {json.dumps(record, indent=2, default=str)}")
            save_document_metadata(record)
            logger.info(f"Successfully saved document metadata for document_title: {record.get('document_title')}, revision: {record.get('revision')}")
        
        logger.info(f"Successfully processed and saved {len(transformed_records)} records from job {job_id}.")
        ch.basic_ack(delivery_tag=method.delivery_tag) # Acknowledge message after successful processing
        
    except Exception as e:
        logger.error(f"Failed to handle metadata_uploaded event for job {job_id}, source {source_file}: {str(e)}")
        logger.error(f"Failed payload: {body.decode() if body else 'No body'}")
        # Re-queue the message for retry
        if ch and ch.is_open and method: # Ensure channel and method are valid before nacking
            ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)
        else:
            logger.error("Channel or method is not available for NACK, message may be lost or require manual intervention.")

def transform_metadata(raw_metadata: dict) -> list:
    """Transform raw metadata from message queue to database format.
    Handles batch messages from bulk-upload-service.
    """
    try:
        transformed_records = []
        source_file = raw_metadata.get('source_file', 'unknown')
        job_id = raw_metadata.get('job_id')
        source = raw_metadata.get('source', 'unknown')
        idempotency_key_header = raw_metadata.get('idempotency_key') # For the batch itself

        # The actual records are in a 'records' list for bulk uploads
        raw_records = raw_metadata.get('records', [])

        if not raw_records:
            logger.warning(f"No records found in message from job {job_id}, source {source_file}")
            return []

        for record in raw_records:
            # Generate a unique idempotency key for each record if not already present
            # This can be a combination of the batch idempotency_key and the record_id
            record_idempotency_key = record.get('idempotency_key', f"{idempotency_key_header}_{record.get('record_id')}")
            
            # Map from canonical schema (ParseRecords.md) to database schema (docUpload.md)
            asset = record.get('asset', {})
            ownership = record.get('ownership', {})
            metadata_fields = record.get('metadata', {}) # Renamed to avoid conflict with 'metadata' variable

            transformed_record = {
                'idempotency_key': record_idempotency_key,
                'transaction_type': raw_metadata.get('transaction_type', 'new'), # Inherit from batch or default
                'brand': metadata_fields.get('brand_id'),
                'business_unit': metadata_fields.get('business_unit'),
                'document_title': asset.get('file_name'),
                'revision': str(asset.get('version')), # Ensure revision is a string as per doc
                'bucket': raw_metadata.get('bucket', 'documents'),
                'object_key': asset.get('storage_path'),
                'content_type': asset.get('file_type'),
                'size_bytes': asset.get('file_size'),
                'checksum': asset.get('checksum'),
                'uploader_id': ownership.get('uploader_user_id'),
                'upload_timestamp': record.get('source', {}).get('job_id'), # Using job_id as a proxy for now, or use current time
                'tags': metadata_fields.get('tags'),
                'description': metadata_fields.get('description'),
                'category': metadata_fields.get('category'),
                'division': metadata_fields.get('division'),
                'document_type': metadata_fields.get('document_type'),
                'region': metadata_fields.get('region'),
                'country': metadata_fields.get('country'),
                'languages': metadata_fields.get('languages'),
                'alternate_part_numbers': metadata_fields.get('alternate_part_numbers'),
                'thumbnail_path': asset.get('thumbnail_path'),
                'expiration_date': asset.get('expiration_date'),
                'acl': ownership.get('acl')
            }
            # Ensure uploader_id is a string
            if transformed_record['uploader_id'] is None:
                transformed_record['uploader_id'] = 'system'

            # Ensure upload_timestamp is a valid datetime string
            if not isinstance(transformed_record['upload_timestamp'], datetime):
                 transformed_record['upload_timestamp'] = datetime.now()


            transformed_records.append(transformed_record)
        
        logger.info(f"Transformed {len(transformed_records)} records from job {job_id}, source {source_file}")
        return transformed_records

    except Exception as e:
        logger.error(f"Failed to transform metadata batch: {str(e)}")
        logger.error(f"Failed raw_metadata: {json.dumps(raw_metadata, indent=2, default=str)}")
        raise

def run_single_upload_listener():
    """Run the single upload event listener in a separate thread"""
    logger.info("Starting single upload event listener...")
    listen_for_events("single-upload.queue", handle_metadata_uploaded_event)

def run_bulk_upload_listener():
    """Run the bulk upload event listener in a separate thread"""
    logger.info("Starting bulk upload event listener...")
    listen_for_events("bulk-upload.queue", handle_metadata_uploaded_event)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Start both event listeners in background threads
    single_upload_thread = threading.Thread(target=run_single_upload_listener, daemon=True)
    bulk_upload_thread = threading.Thread(target=run_bulk_upload_listener, daemon=True)
    
    single_upload_thread.start()
    bulk_upload_thread.start()
    
    logger.info("Both single and bulk upload event listeners started")
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
