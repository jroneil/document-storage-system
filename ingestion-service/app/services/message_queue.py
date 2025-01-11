import pika
import json
import os
from dotenv import load_dotenv

load_dotenv()

def publish_event(event_type: str, payload: dict):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv("RABBITMQ_HOST")))
        channel = connection.channel()
        channel.queue_declare(queue=event_type)
        channel.basic_publish(exchange="", routing_key=event_type, body=json.dumps(payload))
        connection.close()
    except Exception as e:
        raise Exception(f"Failed to publish event: {str(e)}")