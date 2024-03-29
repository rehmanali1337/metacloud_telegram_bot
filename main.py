from telethon.sync import TelegramClient, events
import asyncio
import os
import config
from exts.signal_filters import (
    channel1_filter,
    channel2_filter,
    channel3_filter,
    channel4_filter,
    channel5_filter,
    channel6_filter
)
from exts.executor import SignalExecutor
from exts.mt4 import MT4
import logging
from exts.add_account import AddAccount
import traceback

logger = logging.getLogger()
logger.setLevel(logging.WARNING)
consoleHandler = logging.StreamHandler()
consoleHandler.setLevel(logging.WARNING)
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


async def channel1_handler(message):
    print('Valid Channel 1 signal')
    try:
        signals = channel1_filter(message.raw_text)
    except Exception:
        logger.info('Ignoring signal becuase it is broken!')
        traceback.print_exc()
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel2_handler(message):
    print('Valid Channel 2 signal')
    try:
        signals = channel2_filter(message.raw_text)
    except Exception:
        traceback.print_exc()
        logger.info('Ignoring signal becuase it is broken!')
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel3_handler(message):
    print('Valid Channel 3 signal')
    try:
        signals = channel3_filter(message.raw_text)
    except Exception:
        traceback.print_exc()
        logger.info('Ignoring signal becuase it is broken!')
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel4_handler(message):
    print('Valid Channel 4 signal')
    try:
        signals = channel4_filter(message.raw_text)
    except Exception:
        traceback.print_exc()
        logger.info('Ignoring signal becuase it is broken!')
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


async def channel5_handler(message):
    print('Valid Channel 5 signal')
    try:
        signals = channel5_filter(message.raw_text)
    except Exception:
        traceback.print_exc()
        logger.info('Ignoring signal becuase it is broken!')
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt,  signal)
        await se.start_execution()


async def channel6_handler(message):
    print('Valid Channel 6 signal')
    try:
        signals = channel6_filter(message.raw_text)
    except Exception:
        traceback.print_exc()
        logger.info('Ignoring signal becuase it is broken!')
        return
    mt = MT4()
    await mt.async_init()
    for signal in signals:
        se = SignalExecutor(bot, mt, signal)
        await se.start_execution()


def is_signal(message):
    text = message.raw_text
    if 'tp' in text.lower():
        if 'sl' in text.lower():
            if 'buy' in text.lower() or 'sell' in text.lower():
                return True
    return False


async def setup_event_handlers():
    client.add_event_handler(channel1_handler, events.NewMessage(
        chats=config.CHANNEL1_ID, func=is_signal))
    client.add_event_handler(channel2_handler, events.NewMessage(
        chats=config.CHANNEL2_ID, func=is_signal))
    client.add_event_handler(channel3_handler, events.NewMessage(
        chats=config.CHANNEL3_ID, func=is_signal))
    client.add_event_handler(channel4_handler, events.NewMessage(
        chats=config.CHANNEL4_ID, func=is_signal))
    client.add_event_handler(channel5_handler, events.NewMessage(
        chats=config.CHANNEL5_ID, func=is_signal))
    client.add_event_handler(channel6_handler, events.NewMessage(
        chats=config.CHANNEL6_ID, func=is_signal))


async def after_connect():
    while not client.is_connected():
        await asyncio.sleep(1)
    while not bot.is_connected():
        await asyncio.sleep(1)
    while not await client.is_user_authorized():
        await asyncio.sleep(1)
    while not await bot.is_user_authorized():
        await asyncio.sleep(1)
    await setup_event_handlers()
    print('[+] Client and bot are now connected and authorized!')
    # add_account = AddAccount(bot)
    # await add_account.start()


bot.start(bot_token=config.BOT_TOKEN)
client.start(phone=config.PHONE)
client.loop.create_task(after_connect())
print('[+] Bot is up!')
client.run_until_disconnected()
