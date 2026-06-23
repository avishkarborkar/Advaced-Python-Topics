from event_bus import EventBus
from events import Event, PriceUpdateEvent, VolumeThresholdEvent, TradingHaltEvent
import datetime

class Stock:
    def __init__(self, symbol: str, initial_price: float, event_bus: EventBus):
        self.price = initial_price
        self.symbol = symbol
        self.event_bus = event_bus

    def update_price(self, new_price: float) -> None:
        # First store new price
        # Call the necessary class from Events - symbol name, old/new price
        # Publish to the Event Bus - For announcing

        old_price = self.price
        self.price = new_price
        event = PriceUpdateEvent(stock_symbol = self.symbol, timestamp = datetime.datetime.now()
                                , old_price = old_price, new_price = new_price)
        
        self.event_bus.publish(event=event)

    def update_volume(self, volume: float, threshold: float) -> None:
        event = VolumeThresholdEvent(stock_symbol=self.symbol, timestamp=datetime.datetime.now(), volume=volume, threshold=threshold)

        self.event_bus.publish(event=event)
        
    def halt_trading(self, reason: str) -> None:
        event = TradingHaltEvent(stock_symbol=self.symbol, timestamp=datetime.datetime.now(), reason=reason)
        self.event_bus.publish(event=event)
        
    