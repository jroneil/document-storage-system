import pika
import json
import os
import uuid
from dotenv import load_dotenv
import logging
from app.rabbitmq_utils import get_rabbitmq_connection
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def publish_bulk_upload_message(payload: dict):
    """
    Publish a bulk upload message to RabbitMQ
    
    Args:
        payload: Dictionary containing bulk upload document data
    """
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        # Declare the exchange and queue for bulk uploads
        exchange_name = "uploads.exchange"
        queue_name = "bulk-upload.queue"
        routing_key = "bulk.upload"
        
        channel.exchange_declare(exchange=exchange_name, exchange_type='topic', durable=True)
        channel.queue_declare(queue=queue_name, durable=True)
        channel.queue_bind(exchange=exchange_name, queue=queue_name, routing_key=routing_key)
        
        # Ensure the payload has required fields
        if "idempotency_key" not in payload:
            payload["idempotency_key"] = str(uuid.uuid4())
        if "source" not in payload:
            payload["source"] = "bulk-upload-service"
        if "transaction_type" not in payload:
            payload["transaction_type"] = "new"
        if "bucket" not in payload:
            payload["bucket"] = "documents"
        
        channel.basic_publish(
            exchange=exchange_name,
            routing_key=routing_key,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        logger.info(f"Published bulk upload message to queue: {queue_name}")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to publish bulk upload message: {str(e)}")
        raise
