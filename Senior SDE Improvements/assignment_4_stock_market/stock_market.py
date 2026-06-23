# Expected LEarning Outcomes

# Understanding coupling and cohesion — Can you design systems where objects don't depend on each other?
# Pattern recognition — When should you use Observer? Strategy? Factory?
# SOLID principles — Do you write code that's easy to extend?
# Polymorphism — Can you handle many observer types with one interface?
# Event-driven thinking — Real systems work this way (message queues, event buses, pub/sub)

# Expected Behaviour

# Set up the market
# market = StockMarket(event_bus=EventBus())

# # Create stocks
# apple = Stock(symbol="AAPL", initial_price=150.0)
# market.add_stock(apple)

# # Create observers
# trader = TraderObserver(name="Alice")
# analyst = AnalystObserver(name="Bob")
# logger = LoggerObserver()

# # Subscribe them — market wires everything
# market.add_observer(trader)
# market.add_observer(analyst)
# market.add_observer(logger)

# # Update price — triggers a cascade of events
# market.update_price("AAPL", 152.50)
# # ↓ Stock publishes PriceUpdateEvent
# # ↓ EventBus notifies all subscribed observers
# # ↓ Trader executes trade, Analyst analyzes, Logger records

from event_bus import EventBus
from stocks import Stock
from observers import EventObserver
from events import PriceUpdateEvent, VolumeThresholdEvent, TradingHaltEvent

class StockMarket:

    def __init__(self, event_bus: EventBus):
        self.stocks = {}
        #self.observers = {}
        self.stock_price = 0.0
        self.event_bus = event_bus

    def add_stock(self, stock: Stock):
        self.stocks[stock.symbol] = stock

    def add_observer(self, observer: EventObserver):
        self.event_bus.subscribe(PriceUpdateEvent, observer)
        self.event_bus.subscribe(VolumeThresholdEvent, observer)
        self.event_bus.subscribe(TradingHaltEvent, observer)

    def update_price(self, stock_symbol: str, new_price: float):
        stock: Stock = self.stocks[stock_symbol]
        stock.update_price(new_price=new_price)

    def remove_observer(self, observer: EventObserver):
        self.event_bus.unsubscribe(PriceUpdateEvent, observer)
        self.event_bus.unsubscribe(VolumeThresholdEvent, observer)
        self.event_bus.unsubscribe(TradingHaltEvent, observer)



        
