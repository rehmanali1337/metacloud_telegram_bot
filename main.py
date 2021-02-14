from telethon.sync import TelegramClient, events
import asyncio
import os
import config
from exts.signal_filters import (
    channel1_filter,
    channel2_filter,
    channel3_filter,
    channel4_filter,
    channel5_filter
)
from exts.executor import SignalExecutor
from exts.mt4 import MT4
import logging
from exts.add_account import AddAccount

logger = logging.getLogger()
logger.setLevel(logging.INFO)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.INFO)
formator = logging.Formatter(
    '[%(asctime)s] - [%(name)s] - %(levelname)s - %(message)s')
consoleHandler.setFormatter(formator)
if not os.path.exists('./logs'):
    os.mkdir('logs')
fileHandler = logging.FileHandler('logs/app.log')
fileHandler.setLevel(logging.DEBUG)
fileHandler.setFormatter(formator)
logger.addHandler(fileHandler)
logger.addHandler(consoleHandler)

sessionFiles = './sessionFiles'
if not os.path.exists(sessionFiles):
    os.makedirs(sessionFiles)

client = TelegramClient(f'{sessionFiles}/client',
                        config.API_ID, config.API_HASH)
bot = TelegramClient(f'{sessionFiles}/bot', config.API_ID, config.API_HASH)
mt = MT4()


async def channel1_handler(message):
    print('Valid Channel 1 signal')
    signals = channel1_filter(message.raw_text)
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel2_handler(message):
    print('Valid Channel 2 signal')
    signals = channel2_filter(message.raw_text)
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel3_handler(message):
    print('Valid Channel 3 signal')
    signals = channel3_filter(message.raw_text)
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel4_handler(message):
    print('Valid Channel 4 signal')
    signals = channel4_filter(message.raw_text)
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel5_handler(message):
    print('Valid Channel 5 signal')
    signals = channel5_filter(message.raw_text)
    for signal in signals:
        se = SignalExecutor(bot, mt,  signal)
        await se.start_execution()


def is_signal(message):
    text = message.raw_text
    if 'TP' in text or 'Tp' in text or 'tp' in text:
        return True
    return False


async def setup_event_handlers():
    channel1_name = config.CHANNEL1_NAME
    channel2_name = config.CHANNEL2_NAME
    channel3_name = config.CHANNEL3_NAME
    channel4_name = config.CHANNEL4_NAME
    channel5_name = config.CHANNEL5_NAME
    channel1_id = None
    channel2_id = None
    channel3_id = None
    channel4_id = None
    channel5_id = None
    for d in await client.get_dialogs():
        if d.title == channel1_name:
            channel1_id = d.id
            print('[+] Channel1 found!')
        elif d.title == channel2_name:
            channel2_id = d.id
            print('[+] Channel2 found!')
        elif d.title == channel3_name:
            channel3_id = d.id
            print('[+] Channel3 found!')
        elif d.title == channel4_name:
            channel4_id = d.id
            print('[+] Channel4 found!')
        elif d.title == channel5_name:
            channel5_id = d.id
            print('[+] Channel5 found!')

    if channel1_id:
        client.add_event_handler(channel1_handler, events.NewMessage(
            chats=channel1_id, func=is_signal))
    if channel2_id:
        client.add_event_handler(channel2_handler, events.NewMessage(
            chats=channel2_id, func=is_signal))
    if channel3_id:
        client.add_event_handler(channel3_handler, events.NewMessage(
            chats=channel3_id, func=is_signal))
    if channel4_id:
        client.add_event_handler(channel4_handler, events.NewMessage(
            chats=channel4_id, func=is_signal))
    if channel5_id:
        client.add_event_handler(channel5_handler, events.NewMessage(
            chats=channel5_id, func=is_signal))


async def after_connect():
    while not client.is_connected():
        await asyncio.sleep(1)
    while not bot.is_connected():
        await asyncio.sleep(1)
    while not await client.is_user_authorized():
        await asyncio.sleep(1)
    while not await bot.is_user_authorized():
        await asyncio.sleep(1)
    print('[+] Client and bot are now connected and authorized!')
    await setup_event_handlers()
    add_account = AddAccount(bot)
    await add_account.start()


bot.start(bot_token=config.BOT_TOKEN)
client.start(phone=config.PHONE)
client.loop.create_task(after_connect())
print('[+] Bot is up!')
client.run_until_disconnected()
