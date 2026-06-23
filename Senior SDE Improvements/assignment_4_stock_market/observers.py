# The Observer pattern is about decoupling. Instead of the Stock knowing about traders, analysts, loggers, etc., the Stock just publishes events to a bus, and observers subscribe to those events.

# Why separate observers?

# Each observer has a different job and reacts differently to the same event:

# Observer	Reacts To	Does What
# TraderObserver	PriceUpdateEvent	Executes a trade (e.g., "Price up 5%? Buy!")
# AnalystObserver	PriceUpdateEvent	Records analysis (e.g., "Track trend patterns")
# LoggerObserver	All events	Logs everything for audit trail
# Real example:


# # Price updates to $157.50 (5% increase)
# event = PriceUpdateEvent(stock_symbol="AAPL", old_price=150, new_price=157.5, ...)

# # All three react independently to THE SAME EVENT:
# trader.on_event(event)    # → "Buy AAPL!"
# analyst.on_event(event)   # → "Recorded: bullish signal"
# logger.on_event(event)    # → "Log: AAPL price changed 150→157.5"
# The power: You can add a new observer (e.g., RiskAlertObserver) without touching Stock code. The Stock doesn't care who's listening—it just publishes events.

# Think of it like: A news channel (Stock) broadcasts headlines (events). Traders, analysts, and loggers all tune in and react in their own way. The channel doesn't know or care about them.

from abc import ABC, abstractmethod
from events import Event, PriceUpdateEvent, VolumeThresholdEvent, TradingHaltEvent

class EventObserver(ABC):
    @abstractmethod
    def on_event(self, event: Event):
        pass

class TraderObserver(EventObserver):

    def __init__(self, name: str):
        self.name = name
        self.trades = []

    def on_event(self, event: Event):
        if isinstance(event, PriceUpdateEvent):
            if event.new_price >= event.old_price * 1.05:
                self.trades.append(f"Buy {event.stock_symbol}")
            elif event.new_price < event.old_price * 0.95:
                self.trades.append(f"Sell {event.stock_symbol}")

class LoggerObserver(EventObserver):
    # Logs everything, hence on every cahnge it must be called !
    def __init__(self):
        self.logs = []

    def on_event(self, event):
        self.logs.append(f"{event.stock_symbol} event at {event.timestamp}")

class AlertObserver(EventObserver):
    def __init__(self):
        self.email_alerts = []
    def on_event(self, event: PriceUpdateEvent):
        if event.new_price >= event.old_price * 1.1:
            self.email_alerts.append(f'Price Spike {event.stock_symbol}')

class AnalystObserver(EventObserver):
    def __init__(self, name: str):
        self.name = name
        self.analyses = []

    def on_event(self, event: PriceUpdateEvent):
        if event.new_price >= event.old_price * 1.05:
            self.analyses.append(f'Trend Change {event.stock_symbol} Uptrend')
        else:
            self.analyses.append(f'Trend Change {event.stock_symbol} Downtrend')