import os
import json
import pika
from app.schemas.notification import NotificationRequest
from app.services.email_service import send_email
from app.services.sms_service import send_sms
from app.store.in_memory import InMemoryStore

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def callback(ch, method, properties, body):
    data = json.loads(body)
    payload = NotificationRequest(**data)

    try:
        if payload.type == "email":
            send_email(payload)
        elif payload.type == "sms":
            send_sms(payload)
        elif payload.type == "in-app":
            InMemoryStore.add_notification(payload.userId, {
                "type": "in-app",
                "message": payload.message
            })
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")


def start_worker():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue="notifications", durable=True)
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue="notifications", on_message_callback=callback)

    print("Worker started. Waiting for messages...")
    channel.start_consuming()

if __name__ == "__main__":
    start_worker()
