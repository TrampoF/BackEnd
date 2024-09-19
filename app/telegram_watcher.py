import asyncio
import os
import json
from aio_pika import connect_robust, Message
from telethon import TelegramClient
from telethon.sessions import StringSession


async def monitor_channel(
    api_id, api_hash, chat_identifier, channel_id, channel
):
    async with TelegramClient(StringSession(), api_id, api_hash) as client:
        async for message in client.iter_messages(chat_identifier):
            await channel.default_exchange.publish(
                Message(
                    body=json.dumps(
                        {
                            "chat_identifier": chat_identifier,
                            "message": message.text,
                        }
                    ).encode()
                ),
                routing_key=channel_id,
            )


async def callback(message, channel):
    async with message.process():
        body = json.loads(message.body.decode())
        response_channel = await channel.declare_queue(body["channel_id"], durable=True)
        await monitor_channel(
            int(body["api_id"]),
            body["api_hash"],
            body["chat_identifier"],
            body["channel_id"],
            channel,
        )


async def main():
    # Conecta-se ao RabbitMQ
    connection = await connect_robust(
        host=os.getenv("RABBIT_HOST", "localhost"),
        port=int(os.getenv("RABBIT_PORT", "5672")),
        login=os.getenv("RABBITMQ_DEFAULT_USER", "guest"),
        password=os.getenv("RABBITMQ_DEFAULT_PASS", "guest"),
    )
    channel = await connection.channel()

    queue = await channel.declare_queue("telethon_queue", durable=True)

    await queue.consume(lambda message: callback(message, channel))

    await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
