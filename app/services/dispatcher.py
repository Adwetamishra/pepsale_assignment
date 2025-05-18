import json
import os
import pika
from app.schemas.notification import NotificationRequest
from app.services.email_service import send_email
from app.services.sms_service import send_sms
from app.store.in_memory import InMemoryStore

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def dispatch_notification(payload: NotificationRequest):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST))
    channel = connection.channel()

    channel.queue_declare(queue="notifications", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(payload.dict()),
        properties=pika.BasicProperties(delivery_mode=2),  # Persistent
    )
    connection.close()

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
