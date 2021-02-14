import enum


class SignalTypes(enum.Enum):
    BUY = 'Buy'
    SELL = 'Sell'


class Signal:
    def __init__(self):
        take_profit = None
        stop_loss = None
        price = None
        signal_type = None
        symbol = None
        volume = None
