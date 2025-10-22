import pika
import os
import json
import logging
import uuid
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_rabbitmq_connection():
    """Create a RabbitMQ connection that works in both local and Docker environments"""
    try:
        # Get environment variables with fallbacks
        rabbitmq_user = os.getenv("RABBITMQ_USER", "admin")
        rabbitmq_password = os.getenv("RABBITMQ_PASSWORD", "password")
        
        # Try Docker host first, then localhost if that fails
        hosts_to_try = [
            os.getenv("RABBITMQ_HOST", "rabbitmq"),  # Try Docker service name first
            "localhost"  # Fallback to localhost
        ]
        
        last_exception = None
        for host in hosts_to_try:
            try:
                credentials = pika.PlainCredentials(rabbitmq_user, rabbitmq_password)
                parameters = pika.ConnectionParameters(
                    host=host,
                    port=5672,
                    credentials=credentials,
                    connection_attempts=3,
                    retry_delay=5,
                    heartbeat=600
                )
                connection = pika.BlockingConnection(parameters)
                logger.info(f"Successfully connected to RabbitMQ at {host}")
                return connection
            except Exception as e:
                last_exception = e
                logger.warning(f"Failed to connect to {host}: {str(e)}")
                continue
        
        # If we get here, no connection was successful
        raise Exception(f"Could not connect to RabbitMQ: {str(last_exception)}")
    
    except Exception as e:
        logger.error(f"Error establishing connection: {str(e)}")
        raise

def send_document_upload_message(document_metadata: dict, file_path: str, upload_time: datetime):
    """
    Send a RabbitMQ message when a document is uploaded
    
    Args:
        document_metadata: Dictionary containing document metadata
        file_path: Path to the uploaded file in MinIO
        upload_time: Timestamp when the upload occurred
    """
    connection = None
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare the exchange and queue for single uploads
        exchange_name = "uploads.exchange"
        queue_name = "single-upload.queue"
        routing_key = "single.upload"
        
        channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        
        # Prepare the message according to the specification
        message = {
            "source": "storage-service",
            "idempotency_key": str(uuid.uuid4()),
            "brand": document_metadata.get("brand", ""),
            "business_unit": f"{document_metadata.get('business', '')}/{document_metadata.get('unit', '')}",
            "document_title": document_metadata.get("doc_name", ""),
            "revision": document_metadata.get("revision", ""),
            "bucket": "documents",
            "object_key": file_path,
            "content_type": document_metadata.get("content_type", ""),
            "size_bytes": document_metadata.get("file_size", 0),
            "uploader_id": document_metadata.get("owner_team", ""),
            "upload_timestamp": upload_time.isoformat(),
            "tags": {
                "doc_type": document_metadata.get("doc_type", ""),
                "owner_team": document_metadata.get("owner_team", ""),
                "doc_date": document_metadata.get("doc_date", "")
            }
        }
        
        # Publish the message
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make message persistent
                content_type='application/json'
            )
        )
        
        logger.info(f"Sent single document upload message for file: {file_path}")
        
    except Exception as e:
        logger.error(f"Failed to send RabbitMQ message: {str(e)}")
        raise
    finally:
        if connection and not connection.is_closed:
            connection.close()
