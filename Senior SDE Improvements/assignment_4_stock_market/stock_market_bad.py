"""
Stock Market System — POORLY DESIGNED (TIGHTLY COUPLED)

This is what NOT to do. Everything is hardcoded and tightly coupled.
Your job is to refactor this using the Observer Pattern.
"""
import datetime


class Stock:
    """
    A stock that manages its own notifications.
    PROBLEM: Stock knows about traders, analysts, loggers directly.
    Adding a new observer type means modifying Stock.
    """

    def __init__(self, symbol, initial_price):
        self.symbol = symbol
        self.price = initial_price
        self.traders = []        # hardcoded list of traders
        self.analysts = []       # hardcoded list of analysts
        self.loggers = []        # hardcoded list of loggers

    def add_trader(self, trader):
        self.traders.append(trader)

    def add_analyst(self, analyst):
        self.analysts.append(analyst)

    def add_logger(self, logger):
        self.loggers.append(logger)

    def update_price(self, new_price):
        old_price = self.price
        self.price = new_price

        # TIGHT COUPLING: Stock directly calls observer methods
        for trader in self.traders:
            trader.on_price_change(self.symbol, old_price, new_price)

        for analyst in self.analysts:
            analyst.on_price_change(self.symbol, old_price, new_price)

        for logger in self.loggers:
            logger.on_price_change(self.symbol, old_price, new_price)


class Trader:
    def __init__(self, name):
        self.name = name
        self.trades = []

    def on_price_change(self, symbol, old_price, new_price):
        if new_price > old_price * 1.05:  # 5% increase
            trade = {"symbol": symbol, "action": "buy", "price": new_price}
            self.trades.append(trade)
            print(f"Trader {self.name} executed BUY {symbol} at ${new_price}")


class Analyst:
    def __init__(self, name):
        self.name = name
        self.analyses = []

    def on_price_change(self, symbol, old_price, new_price):
        change_pct = ((new_price - old_price) / old_price) * 100
        analysis = {"symbol": symbol, "change_pct": change_pct}
        self.analyses.append(analysis)
        print(f"Analyst {self.name} noted {symbol} changed {change_pct:.2f}%")


class Logger:
    def __init__(self):
        self.logs = []

    def on_price_change(self, symbol, old_price, new_price):
        log_entry = {
            "symbol": symbol,
            "old_price": old_price,
            "new_price": new_price,
            "timestamp": datetime.datetime.now()
        }
        self.logs.append(log_entry)
        print(f"[LOG] {symbol}: ${old_price} → ${new_price}")


# EXAMPLE: This is the mess
if __name__ == "__main__":
    stock = Stock("AAPL", 150.0)

    trader = Trader("Alice")
    analyst = Analyst("Bob")
    logger = Logger()

    # Hardcoded registration — Stock knows about everyone
    stock.add_trader(trader)
    stock.add_analyst(analyst)
    stock.add_logger(logger)

    # Update price
    stock.update_price(157.5)  # 5% increase

    print(f"\nTrader executed {len(trader.trades)} trades")
    print(f"Analyst made {len(analyst.analyses)} analyses")
    print(f"Logger recorded {len(logger.logs)} events")