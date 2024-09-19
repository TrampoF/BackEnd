import json
import os
import pika
from typing import Any
from app.queue.i_queue import IQueue


class RabbitMQAdapter(IQueue):
    _connection: Any | None
    _channel: Any

    def __init__(self):
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(
                host=os.getenv("RABBIT_HOST", "localhost"),
                port=int(os.getenv("RABBIT_PORT", "5672")),
                credentials=pika.PlainCredentials(
                    os.getenv("RABBITMQ_DEFAULT_USER", "guest"),
                    os.getenv("RABBITMQ_DEFAULT_PASS", "guest"),
                ),
            )
        )
        self._channel = self._connection.channel()

    def get_channel(self):
        yield self._channel

    def disconnect(self):
        self._connection.close()

    def create_exchange(self, exchange: str):
        self._channel.exchange_declare(
            exchange=exchange, exchange_type="direct", durable=True
        )

    def create_queue(self, queue_name: str):
        self._channel.queue_declare(queue=queue_name, durable=True)

    def consume(self, queue_name: str, callback):
        self._channel.basic_consume(
            queue=queue_name, on_message_callback=callback, auto_ack=True
        )

    def publish(self, exchange: str, routing_key: str, body):
        self._channel.basic_publish(
            exchange=exchange, routing_key=routing_key, body=json.dumps(body)
        )

    def make_binding(self, exchange: str, queue_name: str):
        self._channel.queue_bind(exchange=exchange, queue=queue_name)

    def start_consuming(self):
        self._channel.start_consuming()
