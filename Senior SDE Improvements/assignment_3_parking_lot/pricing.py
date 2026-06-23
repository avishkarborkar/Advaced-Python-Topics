from abc import ABC, abstractmethod
import math 

class PricingStrategy(ABC):

    @abstractmethod
    def calculate_fee(self, hours_parked, vehicle_type=None, spot_size=None):
        pass


class HourlyPricing(PricingStrategy):
    def __init__(self, rate_per_hour: float):
        self.rate_per_hour = rate_per_hour

    def calculate_fee(self, hours_parked, vehicle_type=None, spot_size=None):
        hours_parked = max(1, hours_parked)
        return self.rate_per_hour * hours_parked

class DailyPricing(PricingStrategy):
    def __init__(self, rate_per_day: float):
        self.rate_per_day = rate_per_day

    def calculate_fee(self, hours_parked, vehicle_type=None, spot_size=None):
        days = math.ceil(hours_parked / 24)
        days = max(1, days)
        return self.rate_per_day * days


class TieredPricing(PricingStrategy):
    def __init__(self, base_rate, base_hours, overflow_rate):
        self.base_rate = base_rate
        self.base_hours = base_hours
        self.overflow_rate = overflow_rate

    def calculate_fee(self, hours_parked, vehicle_type=None, spot_size=None):
        base_fee = self.base_rate * min(hours_parked, self.base_hours)
        overflow_fee = self.overflow_rate * max(0, hours_parked - self.base_hours)
        return base_fee + overflow_fee

    

# Implements the 'Strategy Pattern', hence if there is a new pricing we can easily add.