import pika
import json
import os
from dotenv import load_dotenv
import logging
from app.rabbitmq_utils import get_rabbitmq_connection
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)


def publish_event(event_type: str, payload: dict):
    try:
        connection = get_rabbitmq_connection()
        channel = connection.channel()
        
        channel.queue_declare(queue=event_type, durable=True)
        
        channel.basic_publish(
            exchange="",
            routing_key=event_type,
            body=json.dumps(payload),
            properties=pika.BasicProperties(
                delivery_mode=2,
                content_type='application/json'
            )
        )
        
        logger.info(f"Published message to queue: {event_type}")
        connection.close()
    except Exception as e:
        logger.error(f"Failed to publish event: {str(e)}")
        raise