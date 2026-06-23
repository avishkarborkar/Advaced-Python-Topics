"""
Tests for Assignment 4 — Stock Market Event System

Run with: python -m pytest test_stock_market.py -v
"""
import pytest
import datetime


# ─────────────────────────────────────────────
# 1. Event System Tests
# ─────────────────────────────────────────────

class TestEventHierarchy:
    """Events represent what happened in the system."""

    def test_event_base_class_exists(self):
        from events import Event
        assert Event is not None

    def test_price_update_event(self):
        from events import PriceUpdateEvent
        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=152.5,
            timestamp=datetime.datetime.now()
        )
        assert event.stock_symbol == "AAPL"
        assert event.old_price == 150.0
        assert event.new_price == 152.5

    def test_volume_threshold_event(self):
        from events import VolumeThresholdEvent
        event = VolumeThresholdEvent(
            stock_symbol="AAPL",
            volume=1000000,
            threshold=500000,
            timestamp=datetime.datetime.now()
        )
        assert event.volume == 1000000
        assert event.threshold == 500000

    def test_trading_halt_event(self):
        from events import TradingHaltEvent
        event = TradingHaltEvent(
            stock_symbol="AAPL",
            reason="Regulatory halt",
            timestamp=datetime.datetime.now()
        )
        assert event.reason == "Regulatory halt"


# ─────────────────────────────────────────────
# 2. Observer/Listener Tests
# ─────────────────────────────────────────────

class TestObserverHierarchy:
    """Observers receive events and act on them."""

    def test_event_observer_base_class_exists(self):
        from observers import EventObserver
        assert EventObserver is not None

    def test_trader_observer_exists(self):
        from observers import TraderObserver
        trader = TraderObserver(name="Alice")
        assert trader.name == "Alice"

    def test_analyst_observer_exists(self):
        from observers import AnalystObserver
        analyst = AnalystObserver(name="Bob")
        assert analyst.name == "Bob"

    def test_logger_observer_exists(self):
        from observers import LoggerObserver
        logger = LoggerObserver()
        assert logger is not None

    def test_trader_reacts_to_price_update(self):
        from observers import TraderObserver
        from events import PriceUpdateEvent
        import datetime

        trader = TraderObserver(name="Alice")
        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=157.5,  # 5% increase
            timestamp=datetime.datetime.now()
        )

        trader.on_event(event)
        # Trader should have executed a trade on 5% increase
        assert len(trader.trades) > 0

    def test_analyst_reacts_to_price_update(self):
        from observers import AnalystObserver
        from events import PriceUpdateEvent
        import datetime

        analyst = AnalystObserver(name="Bob")
        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=152.5,
            timestamp=datetime.datetime.now()
        )

        analyst.on_event(event)
        # Analyst should have recorded analysis
        assert len(analyst.analyses) > 0

    def test_logger_logs_all_events(self):
        from observers import LoggerObserver
        from events import PriceUpdateEvent
        import datetime

        logger = LoggerObserver()
        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=152.5,
            timestamp=datetime.datetime.now()
        )

        logger.on_event(event)
        assert len(logger.logs) > 0


# ─────────────────────────────────────────────
# 3. Event Bus Tests
# ─────────────────────────────────────────────

class TestEventBus:
    """The event bus is the middleman between publishers and subscribers."""

    def test_event_bus_exists(self):
        from event_bus import EventBus
        bus = EventBus()
        assert bus is not None

    def test_subscribe_to_event_type(self):
        from event_bus import EventBus
        from observers import TraderObserver
        from events import PriceUpdateEvent

        bus = EventBus()
        trader = TraderObserver(name="Alice")

        bus.subscribe(PriceUpdateEvent, trader)
        # Should not raise error

    def test_publish_notifies_subscribers(self):
        from event_bus import EventBus
        from observers import TraderObserver
        from events import PriceUpdateEvent
        import datetime

        bus = EventBus()
        trader = TraderObserver(name="Alice")
        bus.subscribe(PriceUpdateEvent, trader)

        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=157.5,
            timestamp=datetime.datetime.now()
        )

        bus.publish(event)
        # Trader should have been notified
        assert len(trader.trades) > 0

    def test_unsubscribe_stops_notifications(self):
        from event_bus import EventBus
        from observers import TraderObserver
        from events import PriceUpdateEvent
        import datetime

        bus = EventBus()
        trader = TraderObserver(name="Alice")
        bus.subscribe(PriceUpdateEvent, trader)
        bus.unsubscribe(PriceUpdateEvent, trader)

        event = PriceUpdateEvent(
            stock_symbol="AAPL",
            old_price=150.0,
            new_price=157.5,
            timestamp=datetime.datetime.now()
        )

        bus.publish(event)
        # Trader should NOT have been notified
        assert len(trader.trades) == 0


# ─────────────────────────────────────────────
# 4. Stock Tests
# ─────────────────────────────────────────────

class TestStock:
    """Stocks publish events, not call observers directly."""

    def test_stock_exists(self):
        from stocks import Stock
        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=None)
        assert stock.symbol == "AAPL"
        assert stock.price == 150.0

    def test_stock_publishes_price_update_event(self):
        from stocks import Stock
        from event_bus import EventBus
        from observers import LoggerObserver
        from events import PriceUpdateEvent

        bus = EventBus()
        logger = LoggerObserver()
        bus.subscribe(PriceUpdateEvent, logger)

        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=bus)
        stock.update_price(152.5)

        # Logger should have received the event
        assert len(logger.logs) > 0

    def test_stock_publishes_volume_threshold_event(self):
        from stocks import Stock
        from event_bus import EventBus
        from observers import LoggerObserver
        from events import VolumeThresholdEvent

        bus = EventBus()
        logger = LoggerObserver()
        bus.subscribe(VolumeThresholdEvent, logger)

        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=bus)
        stock.update_volume(1000000, threshold=500000)

        # Logger should have received the volume threshold event
        assert len(logger.logs) > 0

    def test_stock_does_not_know_about_observers(self):
        """CRITICAL: Stock should NOT have references to observers."""
        from stocks import Stock
        from event_bus import EventBus

        bus = EventBus()
        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=bus)

        # Stock should only know about the event bus, not individual observers
        assert hasattr(stock, 'event_bus')
        assert not hasattr(stock, 'traders')
        assert not hasattr(stock, 'analysts')
        assert not hasattr(stock, 'loggers')


# ─────────────────────────────────────────────
# 5. StockMarket Integration Tests
# ─────────────────────────────────────────────

class TestStockMarket:
    """The market wires stocks and observers together."""

    def test_stock_market_exists(self):
        from stock_market import StockMarket
        from event_bus import EventBus
        market = StockMarket(event_bus=EventBus())
        assert market is not None

    def test_add_stock(self):
        from stock_market import StockMarket
        from stocks import Stock
        from event_bus import EventBus

        market = StockMarket(event_bus=EventBus())
        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=market.event_bus)
        market.add_stock(stock)

        # Should be able to update the stock
        market.update_price("AAPL", 152.5)

    def test_add_observer(self):
        from stock_market import StockMarket
        from observers import TraderObserver
        from stocks import Stock
        from event_bus import EventBus

        market = StockMarket(event_bus=EventBus())
        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=market.event_bus)
        market.add_stock(stock)

        trader = TraderObserver(name="Alice")
        market.add_observer(trader)

        # Update price and observer should react
        market.update_price("AAPL", 157.5)
        assert len(trader.trades) > 0

    def test_multiple_observers_react_independently(self):
        from stock_market import StockMarket
        from observers import TraderObserver, AnalystObserver, LoggerObserver
        from stocks import Stock
        from event_bus import EventBus

        market = StockMarket(event_bus=EventBus())
        stock = Stock(symbol="AAPL", initial_price=150.0, event_bus=market.event_bus)
        market.add_stock(stock)

        trader = TraderObserver(name="Alice")
        analyst = AnalystObserver(name="Bob")
        logger = LoggerObserver()

        market.add_observer(trader)
        market.add_observer(analyst)
        market.add_observer(logger)

        market.update_price("AAPL", 157.5)

        # All observers should have reacted independently
        assert len(trader.trades) > 0
        assert len(analyst.analyses) > 0
        assert len(logger.logs) > 0

    