import time
import pika
import json
import os
import logging
from dotenv import load_dotenv
from ..rabbitmq_utils import get_rabbitmq_connection

load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger(__name__)

def listen_for_events(queue_name: str, callback):
    """Listen for events on the specified queue and process them with the callback function"""
    while True:  # Add reconnection loop
        try:
            connection = get_rabbitmq_connection()
            channel = connection.channel()
            
            logger.info(f"Declaring queue: {queue_name}")
            channel.queue_declare(queue=queue_name, durable=True)
            
            # Set QoS
            channel.basic_qos(prefetch_count=1)

            def on_message(ch, method, properties, body):
                try:
                    logger.info(f"Received message on {queue_name}: {body.decode()}")
                    callback(ch, method, properties, body)
                    ch.basic_ack(delivery_tag=method.delivery_tag)
                except Exception as callback_exception:
                    logger.error(f"Error processing message: {callback_exception}")
                    ch.basic_nack(delivery_tag=method.delivery_tag, requeue=True)

            channel.basic_consume(queue=queue_name, on_message_callback=on_message)
            
            logger.info(f"Starting to consume messages from {queue_name}...")
            channel.start_consuming()
            
        except pika.exceptions.AMQPConnectionError as connection_error:
            logger.error(f"Connection lost: {connection_error}")
            logger.info("Attempting to reconnect in 5 seconds...")
            time.sleep(5)
        except Exception as e:
            logger.exception(f"An unexpected error occurred: {e}")
            raise
