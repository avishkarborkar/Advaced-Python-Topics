from abc import ABC, abstractmethod

class Observer(ABC):
    def __init__(self):
        self.observers = []

    @abstractmethod
    def add_observer(self):
        pass

    @abstractmethod
    def notify(self, msg):
        pass
    

class MsgObserver(Observer):

    def add_observer(self):
        self.add_observer(MsgObserver)

    def notify(self, msg):
        
