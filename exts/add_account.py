from telethon.events import StopPropagation
from telethon import events
from telethon.tl.custom import Button
import os
from exts.mt4 import MT4
import asyncio
import config


def createButton(btnText: str):
    return Button.text(btnText, single_use=True)


async def rm(messages: list):
    for m in messages:
        await m.delete()


def checkFile(payload):
    if payload.message.media != None:
        return True
    return False


def check(checkList):

    def inner(payload):
        button = payload.message.message
        if button in checkList or button == '/start':
            return True
        return False
    return inner


class AddAccount:
    def __init__(self, bot):
        self.bot = bot
        self.mt_version = 5
        self.mt = MT4()

    async def start(self):
        if await self.mt.account_exists():
            return
        async with self.bot.conversation(config.ADMIN_TG_ID, timeout=120) as self.conv:
            await self.conv.send_message('Welcome to the bot!')
            await self.addAccount()
        raise StopPropagation

    async def addAccount(self):
        try:
            q = await self.conv.send_message('Enter your MetaTrader5 account name?')
            r = await self.conv.get_response()
            mtAccountName = r.message
            await rm([q, r])
            q = await self.conv.send_message('Enter your MetaTrader5 login?')
            r = await self.conv.get_response()
            mtLogin = r.message
            await rm([q, r])
            q = await self.conv.send_message('Enter your MetaTrader5 password?')
            r = await self.conv.get_response()
            mtPassword = r.message
            await rm([q, r])
            q = await self.conv.send_message('Enter MetaTrader Server Name?')
            r = await self.conv.get_response()
            await rm([q, r])
            serverName = r.message
            # mt4_video_url = 'https://www.youtube.com/watch?v=PRMpfKunlBw'
            mt5_video_url = 'https://www.youtube.com/watch?v=XXEivPsUC9o'
            btns = [
                Button.url('Where to get the dat file?',
                           url=mt5_video_url)
            ]
            q = await self.conv.send_message('Upload the your broker\'s server file. [*.srv file]?', buttons=btns)
            r = await self.conv.wait_event(events.NewMessage(func=checkFile))
            await rm([q, r])
            await self.conv.send_message('Linking your MT5 Account to the bot.. Please wait ...')
            tempDir = './TempFiles'
            if not os.path.exists(tempDir):
                os.mkdir(tempDir)
            srvFile = await r.download_media(file=f'{tempDir}/')
            profile = await self.mt.getProfileByName(serverName)
            if not profile:
                profile = await self.mt.createProfile(profileName=serverName,
                                                      brokerTimezone=config.BROKER_TIMEZONE,
                                                      brokerDSTSwitchTimezone=config.BROKER_TIMEZONE,
                                                      serversFile=srvFile, version=self.mt_version
                                                      )
            os.remove(srvFile)
            success, addedAccount = await self.mt.createMT4Account(accountName=mtAccountName,
                                                                   accountLogin=mtLogin,
                                                                   accountPassword=mtPassword,
                                                                   serverName=serverName,
                                                                   profileID=profile.id
                                                                   )
            if not success:
                btns = [
                    [
                        createButton('Try Again')
                    ],
                    [
                        createButton('Back')
                    ]
                ]
                await self.conv.send_message('Could not link your account.. Please check your details and try again..', buttons=btns)
                r = await self.conv.wait_event(events.NewMessage(func=check(['Try Again', 'Back'])))
                if r.message.message == 'Try Again':
                    await self.addAccount()
                return
            btns = [
                [
                    createButton('Back')
                ]
            ]
            q = await self.conv.send_message('Account successfully linked to the bot!', buttons=btns)
            r = await self.conv.wait_event(events.NewMessage(func=check(['Back'])))
            res = r.message.message
            await rm([q, r])
            if res == 'Back' or res == '/start':
                await self.addAccount()
                return
        except asyncio.TimeoutError:
            await self.conv.send_message('Response Timeout! Please start again!')
            self.conv.cancel()
