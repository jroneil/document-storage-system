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


def listen_for_events(event_type: str, callback):
    """
    Listen for events from RabbitMQ queue with automatic reconnection.
    
    Args:
        event_type: The queue name to listen to
        callback: Function to handle incoming messages
    """
    import time
    
    while True:  # Add reconnection loop
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()
            
            logger.info(f"Declaring queue: {event_type}")
            channel.queue_declare(queue=event_type, durable=True)
            
            # Set QoS
            channel.basic_qos(prefetch_count=1)

            def on_message(ch, method, properties, body):
                try:
                    logger.info(f"Received message on {event_type}: {body.decode()}")
                    callback(ch, method, properties, body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as callback_exception:
                    logger.error(f"Error processing message: {callback_exception}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(queue=event_type, on_message_callback=on_message)
            
            logger.info(f"Starting to consume messages from {event_type}...")
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError as connection_error:
            logger.error(f"Connection lost: {connection_error}")
            logger.info("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            raise
