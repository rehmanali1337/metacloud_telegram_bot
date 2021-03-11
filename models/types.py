import enum


class SignalTypes(enum.Enum):
    BUY = 'Buy'
    SELL = 'Sell'


class Signal:
    def __init__(self):
        self.take_profit = None
        self.stop_loss = None
        self.price = None
        self.signal_type = None
        self.symbol = None
        self.volume = None
