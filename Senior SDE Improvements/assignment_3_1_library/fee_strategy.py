from abc import ABC, abstractmethod
from items import LibraryItem, DVD

class LateFeeStrategy(ABC):
    
    @abstractmethod
    def calculate_fee(self, days_late: int, item_type: LibraryItem = None):
        pass


class FlatDailyFee(LateFeeStrategy):
    def __init__(self, rate_per_day: float):
        self.rate_per_day = rate_per_day

    def calculate_fee(self, days_late: int, item_type = None):
        return self.rate_per_day * days_late
    

class NoFee(LateFeeStrategy):
    def calculate_fee(self, days_late, item_type = None):
        return 0.0

class TieredFee(LateFeeStrategy):
    def __init__(self, base_rate: float, base_days: float, overflow_rate: float):
        self.base_rate = base_rate
        self.base_days = base_days
        self.overflow_rate = overflow_rate
    
    def calculate_fee(self, days_late, item_type = None):
        base_fee = self.base_rate * min(days_late, self.base_days)
        overflow_fee = self.overflow_rate * max(0, days_late - self.base_days)
        return base_fee + overflow_fee


# MAde 
class DvDFee(LateFeeStrategy):
    def __init__(self, rate_per_day: float):
        self.rate_per_day = rate_per_day

    def calculate_fee(self, days_late: int, item_type = None):
        if isinstance(item_type, DVD):
            return 2*days_late*self.rate_per_day
        else:
            raise ValueError("Not a DvD")