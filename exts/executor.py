import json
from telethon import TelegramClient, events
from models.types import Signal, SignalTypes
from telethon.tl.custom.button import Button
import asyncio
import config
from exts.mt4 import MT4


class SignalExecutor:
    def __init__(self, bot: TelegramClient, mt, signal: Signal,):
        self.bot = bot
        self.admin_id = config.ADMIN_TG_ID
        self.signal = signal
        self.mt = mt
        self.execution_channels = [1, 3, 4, 5]

    async def start_execution(self):
        if self.signal.channel_number in self.execution_channels:
            await self.execute_signal()
            return
        await self.ask_for_confirmation()

    async def execute_signal(self):
        if self.signal.signal_type == SignalTypes.BUY:
            print('Executing buy order ...')
            await self.mt.create_buy_order(symbol=self.signal.symbol,
                                           stop_loss=self.signal.stop_loss,
                                           take_profit=self.signal.take_profit,
                                           open_price=self.signal.price)
        elif self.signal.signal_type == SignalTypes.SELL:
            print('Executing sell order ...')
            await self.mt.create_sell_order(symbol=self.signal.symbol,
                                            stop_loss=self.signal.stop_loss,
                                            take_profit=self.signal.take_profit,
                                            open_price=self.signal.price)

    async def ask_for_confirmation(self):
        async with self.bot.conversation(self.admin_id, timeout=240) as self.conv:
            execute_btn = Button.inline('Execute Signal', data=b'execute')
            not_execute_btn = Button.inline(
                'Don\'t Execute Signal', data=b'not_execute')
            buttons = [execute_btn, not_execute_btn]
            message = f'New Signal\nSymbol : {self.signal.symbol}\n{self.signal.signal_type.value}@{self.signal.price}\n\
Price : {self.signal.price}\nStop Loss : \
{self.signal.stop_loss}\nTake Profit : {self.signal.take_profit}'

            q = await self.conv.send_message(message, buttons=buttons)
            try:
                r = await self.conv.wait_event(events.CallbackQuery)
                await q.delete()
                if r.query.data == b'execute':
                    await self.execute_signal()
                elif r.query.data == b'not_execute':
                    self.conv.cancel()
                    return
            except asyncio.TimeoutError:
                if self.signal.channel_number in self.execution_channels:
                    await self.execute_signal()
                    message = message + '\n\n**Auto-Executed**'
                    await q.delete()
                    await self.conv.send_message(message)
                    return
                message = message + '\n\n**Terminated**'
                await q.delete()
                await self.conv.send_message(message)
