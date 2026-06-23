from events import Event
from observers import EventObserver

class EventBus():
    def __init__(self):
        self.subscribed = {}

    def subscribe(self, event_type: Event, observer: EventObserver):
        # Check if the event type exists, and create a list if it doesn't:
        if event_type not in self.subscribed:
            self.subscribed[event_type] = []
        self.subscribed[event_type].append(observer)

    def unsubscribe(self, event_type: Event, observer: EventObserver):
        self.subscribed[event_type].remove(observer)


    def publish(self, event: Event):
        # Using this we can get the actual class being called from the Base Abstract Class
        event_type = event.__class__
        if event_type in self.subscribed:
            for observer in self.subscribed[event_type]:
                observer.on_event(event)

        

# event = PriceUpdateEvent(
#     stock_symbol="AAPL",
#     timestamp=datetime.now(),
#     old_price=150.0,
#     new_price=157.5  # 5% increase
# )
        
#event_type = event.__class__  # Gets PriceUpdateEvent (the class)

#if event_type in self.subscribed:  # Check: is PriceUpdateEvent in the dict?
    # YES! PriceUpdateEvent is in subscribed
    
    #for observer in self.subscribed[event_type]:
        # Loop: trader, analyst, logger
        
        #observer.on_event(event)  # Call each one
        # trader.on_event(event) → trader buys (5% increase!)
        # analyst.on_event(event) → analyst records uptrend
        # logger.on_event(event) → logger logs the event