from telethon.sync import TelegramClient, events
import json
import asyncio
import config


client = TelegramClient('sessionFiles/client', config.API_ID, config.API_HASH)


async def on_ready():
    while not client.is_connected():
        await asyncio.sleep(1)
    while not await client.is_user_authorized():
        await asyncio.sleep(1)
    username = input('Enter the username to get the telegram ID : ')
    en = await client.get_entity(username)
    print(f'ID : {en.id}')

try:
    client.start(phone=config.PHONE)
    client.loop.create_task(on_ready())
    print(' Bot is up!')
    client.run_until_disconnected()
except KeyboardInterrupt:
    print('Exiting ...')
    exit()
