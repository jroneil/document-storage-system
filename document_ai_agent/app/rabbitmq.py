import pika
import json
from . import app

def publish_message(message):
    """
    Publishes a message to the RabbitMQ queue.
    """
    try:
        # Create a connection to RabbitMQ
        credentials = pika.PlainCredentials(app.config['RABBITMQ_USER'], app.config['RABBITMQ_PASSWORD'])
        connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=app.config['RABBITMQ_HOST'],
                port=app.config['RABBITMQ_PORT'],
                credentials=credentials
            )
        )
        channel = connection.channel()

        # Declare the queue
        channel.queue_declare(queue=app.config['RABBITMQ_QUEUE'], durable=True)

        # Publish the message
        channel.basic_publish(
            exchange='',
            routing_key=app.config['RABBITMQ_QUEUE'],
            body=json.dumps(message),
            properties=pika.BasicProperties(
                delivery_mode=2,  # Make the message persistent
            )
        )

        print(f"Published message: {message}")
        connection.close()
    except Exception as e:
        print(f"Failed to publish message: {e}")