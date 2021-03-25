# from models.types import Signal, SignalTypes
import enum
import re
from models.types import SignalTypes, Signal


def channel1_filter(signal):
    print('Filtering the below signal in channel 1 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 1
    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    else:
        sig.symbol = re.match(r'(^\w+)', signal).group()
    order_type = re.match(r'(^\w+) (\w+)', signal).group(2).lower()
    if order_type == 'buy':
        sig.signal_type = SignalTypes.BUY
    elif order_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    if 'TP ' in signal:
        # Only one signal in this case
        sig.take_profit = re.search(
            r'TP\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
        sig.stop_loss = re.search(
            r'SL\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
        sig.price = re.search(r'@\D*(\d*\.?\d*)', signal,
                              flags=re.IGNORECASE).group(1)
        return [sig]
    sig.price = re.search(r'@\D*(\d*\.?\d*)', signal).group(1)
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
        return [sig, sig2]
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
    else:
        sig.symbol = re.match(
            r'(^\w+)', signal, flags=re.IGNORECASE).group(1).upper()
    signal_type = re.search(r'^\w+ (\w+)', signal,
                            flags=re.IGNORECASE).group(1).lower()
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY
    sig.price = re.search(r'at\D*(\d*\.?\d*)', signal).group(1)
    sig.stop_loss = re.search(r'SL\D*(\d*\.?\d*)', signal,
                              flags=re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d*\.?\d*)', signal, flags=re.IGNORECASE).group(1)
    return [sig]


def channel3_filter(signal):
    print('Filtering the below signal in channel 3 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 3
    signal_type = re.match(r'(^\w+)', signal).group(1).lower()
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    else:
        sig.symbol = re.search(r'(\w+) (\w+)', signal,
                               re.IGNORECASE).group().split(' ')[-1].upper()
    sig.stop_loss = re.search(
        r'sl\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.price = re.search(r'^\w* \w*\D*(\d*\.?\d*)',
                          signal, re.IGNORECASE).group(1)
    return [sig]


def channel4_filter(signal):
    print('Filtering the below signal in channel 4 filter function...')
    print(signal)
    sig = Signal()
    sig.channel_number = 4
    signal_type = re.match(r'\w+', signal, re.IGNORECASE).group().lower()
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY

    if 'oil' in signal.lower():
        sig.symbol = 'XTIUSD'
    elif 'gold' in signal.lower():
        sig.symbol = 'XAUUSD'
    else:
        sig.symbol = re.findall(r'(\w+)', signal.split('\n')
                                [0])[-1].upper().strip()
    sig.stop_loss = re.search(
        r'sl\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'tp\D*(\d+\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.price = re.search(r'now (\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    if 'one more' in signal.lower():
        sig2 = Signal()
        sig2.channel_number = 4
        sig2.stop_loss = sig.stop_loss
        sig2.take_profit = sig.take_profit
        sig2.signal_type = sig.signal_type
        sig2.symbol = sig.symbol
        sig2.price = re.search(
            r'one more (\w+)+\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(2)
        return [sig, sig2]
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
    else:
        sig.symbol = re.search(
            r'#(\w+)', signal, re.IGNORECASE).group(1).upper()
    res = re.search(r'#\w+\s(\w+)_(\d*\.?\d*)', signal, re.IGNORECASE)
    sig.price = res.group(2)
    signal_type = res.group(1).lower()
    if signal_type == 'sell':
        sig.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        sig.signal_type = SignalTypes.BUY
    sig.stop_loss = re.search(
        r'SL\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    sig.take_profit = re.search(
        r'TP\D*(\d*\.?\d*)', signal, re.IGNORECASE).group(1)
    if 'one more' in signal.lower():
        sig2 = Signal()
        sig.channel_number = 5
        sig2.symbol = sig.symbol
        sig2.take_profit = sig.take_profit
        sig2.stop_loss = sig.stop_loss
        res = re.search(
            r'one more (\w+)\D*(\d*\.?\d*)', signal, re.IGNORECASE)
        sig2.price = res.group(2)
        signal_type = res.group(1).lower().split('_')[0]
        print(signal_type)
        if signal_type == 'sell':
            sig2.signal_type = SignalTypes.SELL
        elif signal_type == 'buy':
            sig2.signal_type = SignalTypes.BUY
        return [sig, sig2]
    return [sig]
