from telethon.sync import TelegramClient, events
import json
import asyncio

config = json.load(open('config.json', 'r'))

API_ID = config.get('API_ID')
API_HASH = config.get('API_HASH')
PHONE = config.get('PHONE')

client = TelegramClient('sessionFiles/client', API_ID, API_HASH)


async def on_ready():
    while not client.is_connected():
        await asyncio.sleep(1)
    while not await client.is_user_authorized():
        await asyncio.sleep(1)
    username = input('Enter the username to get the telegram ID : ')
    en = await client.get_entity(username)
    print(f'ID : {en.id}')

try:
    client.start(phone=PHONE)
    client.loop.create_task(on_ready())
    print(' Bot is up!')
    client.run_until_disconnected()
except KeyboardInterrupt:
    print('Exiting ...')
    exit()
