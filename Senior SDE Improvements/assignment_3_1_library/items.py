from abc import ABC, abstractmethod

class LibraryItem(ABC):

    def __init__(self, item_id: str, title: str) -> None: 
        self.item_id = item_id
        self.title = title

    @property
    @abstractmethod
    def loan_period_days(self):
        pass

class Book(LibraryItem):
    @property
    def loan_period_days(self):
        return 14

class Magazine(LibraryItem):
    @property
    def loan_period_days(self):
        return 7

class DVD(LibraryItem):
    @property
    def loan_period_days(self):
        return 3
    


# So here we are having a factory pattern for Every Item (Book, DVD, Magzien)
# And the Baseclass only initiallisez the Item's ID and Title

# Makes sense because Book, Mag and DvD require a Title and ID, and there can be multiple instances hence we 
# have the base class