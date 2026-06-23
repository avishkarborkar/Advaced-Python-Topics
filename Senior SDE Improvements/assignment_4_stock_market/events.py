# Let's create an abstract class called Event that stores PRiceUpdates, VolumeThresholds, TradingHaltEvent
# This creates objects for every stock that stores these individual values.
# We can mutate the objects created usign this class by calling the following sub class methods

# This allows us to loosely couple the base class Stock

# example:
# event = PriceUpdateEvent(stock_symbol="AAPL", old_price=150.0, new_price=152.5, timestamp=...)


from abc import ABC, abstractmethod
import datetime

class Event(ABC):
    def __init__(self, stock_symbol: str, timestamp: datetime.datetime):
        self.stock_symbol = stock_symbol
        self.timestamp = timestamp

class PriceUpdateEvent(Event):
    def __init__(self, stock_symbol: str, timestamp: datetime.datetime, old_price: float, new_price: float):
        super().__init__(stock_symbol, timestamp)
        self.old_price = old_price
        self.new_price = new_price


class VolumeThresholdEvent(Event):
    def __init__(self, stock_symbol: str, timestamp: datetime.datetime, volume: float, threshold: float):
        super().__init__(stock_symbol, timestamp)
        self.volume = volume
        self.threshold = threshold

class TradingHaltEvent(Event):
    def __init__(self, stock_symbol: str, timestamp: datetime.datetime, reason: str):
        super().__init__(stock_symbol, timestamp)
        self.reason = reason