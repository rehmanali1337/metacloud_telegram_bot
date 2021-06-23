# from models.types import Signal, SignalTypes
import enum
import re
from models.types import SignalTypes, Signal
from Utils.utils import contains_non_digit, non_digitize


def channel1_filter(signal):
    print('Filtering the below signal in channel 1 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 1
    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.match(r'(^\w+)', signal).group(1)
    if 'buy' in signal.lower():
        sig.signal_type = SignalTypes.BUY
    elif 'sell' in signal.lower():
        sig.signal_type = SignalTypes.SELL
    if 'TP ' in signal:
        # Only one signal in this case
        sig.take_profit = re.search(
            r'TP\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
        sig.stop_loss = re.search(
            r'SL\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
        if sig.signal_type == SignalTypes.SELL:
            sig.price = re.search(r'sell\D*(\d*\.?\d*)', signal,
                                  flags=re.IGNORECASE).group(1)
        elif sig.signal_type == SignalTypes.BUY:
            sig.price = re.search(r'buy\D*(\d*\.?\d*)', signal,
                                  flags=re.IGNORECASE).group(1)

        return [sig]
    sig.price = re.search(r'^\D*(\d*\.?\d*)', signal).group(1)
    sig.stop_loss = re.search(r'SL\D*(\d*\.?\d*)', signal,
                              flags=re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'TP1 (\d*\.?\d+)', signal, flags=re.IGNORECASE).group(1)
    if 'TP3 ' in signal:
        sig2 = Signal()
        sig.channel_number = 1
        sig2.price = sig.price
        sig2.stop_loss = sig.stop_loss
        sig2.signal_type = sig.signal_type
        sig2.symbol = sig.symbol
        sig2.take_profit = re.search(
            r'TP3 \D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
        print_signals([sig, sig2])
        return [sig, sig2]
    print_signals([sig])
    return [sig]


def channel2_filter(signal):
    print('Filtering the below signal in channel 2 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 2

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.match(
            r'(^\w+)', signal, flags=re.IGNORECASE).group(1).upper()

    if 'sell' in signal.lower():
        sig.signal_type = SignalTypes.SELL
    elif 'buy' in signal.lower():
        sig.signal_type = SignalTypes.BUY

    sig.price = re.search(r'\D*(\d*\.?\d*)', signal).group(1)
    sig.stop_loss = re.search(r'SL\D*(\d*\.?\d*)', signal,
                              flags=re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
    print_signals([sig])
    return [sig]


def channel3_filter(signal):
    print('Filtering the below signal in channel 3 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 3
    if 'sell' in signal.lower():
        sig.signal_type = SignalTypes.SELL
    elif 'buy' in signal.lower():
        sig.signal_type = SignalTypes.BUY

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.search(r'(\w+)\s+(\w+)', signal,
                               re.IGNORECASE).group().split(' ')[-1].upper()
    sig.stop_loss = re.search(
        r'sl\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    if 'tp1' in signal.lower():
        sig.take_profit = re.search(
            r'tp1\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    else:
        sig.take_profit = re.search(
            r'tp\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.price = re.search(r'^\w*\s+\w*\D*(\d*\.?\d*)',
                          signal, re.IGNORECASE).group(1)
    print_signals([sig])
    return [sig]


def channel4_filter(signal):
    print('Filtering the below signal in channel 4 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 4
    first_line = signal.split('\n')[0]
    signal_type = 'buy' if 'buy' in first_line.lower() else 'sell'
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.findall(r'(\w+)', signal.split('\n')
                                [0])[-1].upper().strip()
    sig.stop_loss = re.search(
        r'sl\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d+\.?\d*)', signal, re.IGNORECASE).group(1)
    try:
        sig.price = re.search(r'now (\d*\.?\d*)', signal,
                              re.IGNORECASE).group(1)
    except AttributeError:
        if sig.signal_type == SignalTypes.BUY:
            sig.price = re.search(r'buy\D*(\d*\.?\d*)',
                                  signal, re.IGNORECASE).group(1)
        elif sig.signal_type == SignalTypes.SELL:
            sig.price = re.search(r'sell\D*(\d*\.?\d*)',
                                  signal, re.IGNORECASE).group(1)
    if 'one more' in signal.lower():
        sig2 = Signal()
        sig2.channel_number = 4
        sig2.stop_loss = sig.stop_loss
        sig2.take_profit = sig.take_profit
        sig2.signal_type = sig.signal_type
        sig2.symbol = sig.symbol
        sig2.price = re.search(
            r'one more (\w+)+\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(2)
        print_signals([sig, sig2])
        return [sig, sig2]
    print_signals([sig])
    return [sig]


def channel5_filter(signal):
    print('Filtering the below signal in channel 5 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 5
    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.search(
            r'^#?(\w+)', signal, re.IGNORECASE).group(1).upper()
    if 'sell' in signal.lower():
        sig.signal_type = SignalTypes.SELL
        sig.price = re.search(r'sell_*(\d*\.?\d*)', signal,
                              re.IGNORECASE).group(1)
    elif 'buy' in signal.lower():
        sig.signal_type = SignalTypes.BUY
        sig.price = re.search(r'buy_(\d*\.?\d*)', signal,
                              re.IGNORECASE).group(1)
    assert sig.price.isdigit()
    sig.stop_loss = re.search(
        r'SL\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'TP\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    if 'one more' in signal.split('\n')[2].lower():
        sig2 = Signal()
        sig2.channel_number = 5
        sig2.symbol = sig.symbol
        sig2.take_profit = sig.take_profit
        sig2.stop_loss = sig.stop_loss
        res = re.search(
            r'one more \D*(\d*\.?\d*)', signal, re.IGNORECASE)
        sig2.price = res.group(1)
        if 'sell' in signal.split('\n')[2].lower():
            sig2.signal_type = SignalTypes.SELL
        if 'buy' in signal.lower().split('\n')[2]:
            sig2.signal_type = SignalTypes.BUY
        print_signals([sig, sig2])
        return [sig, sig2]
    print_signals([sig])
    return [sig]


def channel6_filter(signal):
    print('Filtering the below signal in channel 6 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 4
    first_line = signal.split('\n')[0]
    signal_type = 'buy' if 'buy' in first_line.lower() else 'sell'
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    elif 'de30' in signal.lower() or 'ger30' in signal.lower() or 'dax30' in signal.lower():
        sig.symbol = 'DE30'
    elif 'dxy' in signal.lower():
        sig.symbol = 'DXY_M1'
    elif 'nasdaq' in signal.lower():
        sig.symbol = 'US100'
    else:
        sig.symbol = re.findall(r'(\w+)', signal.split('\n')
                                [0])[-1].upper().strip()

    sig.stop_loss = re.search(
        r'sl\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d+\.?\d*)', signal, re.IGNORECASE).group(1)
    try:
        sig.price = re.search(r'now (\d*\.?\d*)', signal,
                              re.IGNORECASE).group(1)
    except AttributeError:
        if sig.signal_type == SignalTypes.BUY:
            sig.price = re.search(r'buy\D*(\d*\.?\d*)',
                                  signal, re.IGNORECASE).group(1)
        elif sig.signal_type == SignalTypes.SELL:
            sig.price = re.search(r'sell\D*(\d*\.?\d*)',
                                  signal, re.IGNORECASE).group(1)
    if 'one more' in signal.lower():
        sig2 = Signal()
        sig2.channel_number = 4
        sig2.stop_loss = sig.stop_loss
        sig2.take_profit = sig.take_profit
        sig2.signal_type = sig.signal_type
        sig2.symbol = sig.symbol
        sig2.price = re.search(
            r'one more (\w+)+\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(2)
        print_signals([sig, sig2])
        return [sig, sig2]
    print_signals([sig])
    return [sig]


def print_signals(signals):
    for signal in signals:
        print(
            f'------------<Signal {signals.index(signal) +1}>----------------')
        print(f'Channel Number : {signal.channel_number}')
        print('Stop Loss : ', signal.stop_loss)
        print('Take Profit : ', signal.take_profit)
        print('Signal Type : ', signal.signal_type)
        print('Symbol : ', signal.symbol)
        print('Price : ', signal.price)
        print('\n\n')
