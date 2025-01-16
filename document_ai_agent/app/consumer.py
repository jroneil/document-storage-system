#for info purposes only add to  the consumer app
import pika
import json
from app import app

def consume_messages():
    """
    Consumes messages from the RabbitMQ queue.
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

        # Define a callback function to process messages
        def callback(ch, method, properties, body):
            message = json.loads(body)
            print(f"Received message: {message}")
            # Acknowledge the message
            ch.basic_ack(delivery_tag=method.delivery_tag)

        # Start consuming messages
        channel.basic_consume(queue=app.config['RABBITMQ_QUEUE'], on_message_callback=callback)
        print("Waiting for messages. To exit, press CTRL+C")
        channel.start_consuming()
    except Exception as e:
        print(f"Failed to consume messages: {e}")

if __name__ == '__main__':
    consume_messages()