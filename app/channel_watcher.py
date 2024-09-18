from telethon import TelegramClient


client = TelegramClient("anon", 1, "anon")


async def main():
    client.connect()

    async for message in client.iter_messages("me"):
        print(message.id, message.text)


with client:
    client.loop.run_until_complete(main())
