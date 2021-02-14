# from models.types import Signal, SignalTypes
import enum


class SignalTypes(enum.Enum):
    BUY = 'buy'
    SELL = 'sell'


class Signal:
    def __init__(self):
        take_profit = None
        stop_loss = None
        price = None
        signal_type = None
        symbol = None


def channel1_filter(signal: str) -> list:
    all_signals = list()
    s = Signal()
    s.symbol = signal.split(' ')[0].strip()
    signal_type = signal.split(' ')[1].lower().strip()
    if signal_type == 'sell':
        s.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        s.signal_type = SignalTypes.BUY
    s.price = signal.split('@')[1].split('\n')[0].strip()
    s.stop_loss = signal.split('\n')[1].split(' ')[1].strip()
    s.take_profit = signal.split('\n')[2].split(' ')[1].strip()
    all_signals.append(s)
    if 'TP3' in signal:
        s2 = Signal()
        s2.take_profit = signal.split('\n')[-1].split(' ')[-1]
        s2.stop_loss = s.stop_loss
        s2.price = s.price
        s2.symbol = s.symbol
        s2.signal_type = s.signal_type
        all_signals.append(s2)
    return all_signals


def channel2_filter(signal: str) -> list:
    s = Signal()
    s.symbol = signal.split(' ')[0].upper()
    signal_type = signal.split(' ')[1].strip().lower()
    if signal_type == 'sell':
        s.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        s.signal_type = SignalTypes.BUY
    s.price = signal.split('at')[1].split('\n')[0].strip()
    s.stop_loss = signal.split('Sl')[1].split('\n')[0].strip()
    s.take_profit = signal.split('Tp')[1].strip()
    return [s]


def channel3_filter(signal: str) -> []:
    # TODO: Have some doubts in function.. Needs to be worked on.
    # Will need to talk to client for fix
    s = Signal()
    signal_type = signal.split(' ')[0].strip().lower()
    if signal_type == 'sell':
        s.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        s.signal_type = SignalTypes.BUY
    s.stop_loss = signal.split('\n')[2].split('..')[-1].strip()
    s.take_profit = signal.split('\n')[3].split('..')[-1].strip()
    s.price = signal.split('\n')[0].split('AT')[-1].strip()
    s.symbol = signal.split(' ')[1].upper()
    return [s]


def channel4_filter(signal: str) -> []:
    all_signals = []
    s = Signal()
    signal_type = signal.split(' ')[0].strip().lower()
    if signal_type == 'sell':
        s.signal_type = SignalTypes.SELL
    elif signal_type == 'buy':
        s.signal_type = SignalTypes.BUY
    s.symbol = signal.split(' ')[2].split('\n')[0].strip().upper()
    s.stop_loss = signal.split('\n')[3].split('..')[-1].strip()
    s.take_profit = signal.split('\n')[-2].split('..')[-1].strip()
    all_signals.append(s)
    if 'more' in signal:
        s2 = Signal()
        s2.price = signal.split('\n')[2].split('at')[-1].strip()
        s2.take_profit = s.take_profit
        s2.stop_loss = s.stop_loss
        s2.symbol = s.symbol
        s2.signal_type = s.signal_type
        all_signals.append(s2)
    return all_signals


def channel5_filter(signal: str) -> []:
    all_signals = []
    s = Signal()
    signal_type = signal.split('\n')[1].split('_')[0].strip().lower()
    if signal_type == 'buy':
        s.signal_type = SignalTypes.BUY
    elif signal_type == 'sell':
        s.signal_type = SignalTypes.SELL
    s.symbol = signal.split('\n')[0].replace('#', '').strip().upper()
    s.price = signal.split('\n')[1].split('_')[1].strip()
    s.stop_loss = signal.split('\n')[3].split('_')[-1].strip()
    s.take_profit = signal.split('\n')[4].split('_')[-1].strip()
    all_signals.append(s)
    if 'MORE' in signal:
        # Get another signal with another price but same tp and sl.
        s2 = Signal()
        s2.price = signal.split('\n')[2].split('_')[-1].strip()
        s2.take_profit = s.take_profit
        s2.stop_loss = s.stop_loss
        s2.signal_type = s.signal_type
        s2.symbol = s.symbol
        all_signals.append(s2)
    return all_signals


signal = '''#USDCAD
SELL_1.2775
ONE MORE SELL_1.2825
SL_1.2875
TP_1.2740
TP2_1.2675'''

channel5_filter(signal)
