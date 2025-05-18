import os
import pika
import json

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "localhost")

def send_to_queue(data: dict):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(host=RABBITMQ_HOST)
    )
    channel = connection.channel()

    channel.queue_declare(queue="notifications", durable=True)
    channel.basic_publish(
        exchange="",
        routing_key="notifications",
        body=json.dumps(data),
        properties=pika.BasicProperties(
            delivery_mode=2,
        ),
    )
    connection.close()
