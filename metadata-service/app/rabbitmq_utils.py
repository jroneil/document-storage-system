import pika
import os
import logging
from dotenv import load_dotenv

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
