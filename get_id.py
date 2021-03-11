from telethon.sync import TelegramClient, events
from telethon.tl.types import PeerChannel
import json
import asyncio
import config


client = TelegramClient('sessionFiles/client', config.API_ID, config.API_HASH)


async def get_entity_by_username():
    username = input('\nEnter the username to get the telegram ID : ')
    en = await client.get_entity(username)
    print(f'\nUser ID : {en.id}')


def check_forward(message):
    if message.message.fwd_from is None:
        return False
    return True


async def print_id(message):
    type_of_en = message.fwd_from.from_id
    if isinstance(type_of_en, PeerChannel):
        print(f'\nChannel ID : {type_of_en.channel_id}')


async def get_entity_by_message_forward():
    print('\nGo to the channel whose ID you want to get and \
forward a message from that channel to somewhere else.\n')
    client.add_event_handler(print_id, events.NewMessage(func=check_forward))


async def on_ready():
    while not client.is_connected():
        await asyncio.sleep(1)
    while not await client.is_user_authorized():
        await asyncio.sleep(1)
    print('You can get telegram ID of Group/Channel/User using this script.')
    print('1. Get User ID')
    print('2. Get Channel ID')
    while True:
        user_in = int(input('Enter 1 or 2 : '))
        if user_in not in [1, 2]:
            continue
        break
    if user_in == 1:
        await get_entity_by_username()
    elif user_in == 2:
        await get_entity_by_message_forward()

try:
    client.start(phone=config.PHONE)
    client.loop.create_task(on_ready())
    client.run_until_disconnected()
except KeyboardInterrupt:
    print('Exiting ...')
    exit()
