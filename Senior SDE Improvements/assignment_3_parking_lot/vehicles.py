from abc import ABC, abstractmethod

class Vehicle(ABC):
    def __init__(self, license_plate: dict):
        self.license_plate = license_plate

    @property
    @abstractmethod
    def allowed_spot_sizes(self):
        pass

class Motorcycle(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    @property
    def allowed_spot_sizes(self):
       return ["small", "medium", "large"] 
    
class Car(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    @property
    def allowed_spot_sizes(self):
        return ["medium", "large"] 

class Truck(Vehicle):
    def __init__(self, license_plate):
        super().__init__(license_plate)
    
    @property
    def allowed_spot_sizes(self):
        return ["large"] 
    


# In V1 the problems in the code I wrote:

# 1. I was dirctly instatiating the Class Vehicle, Later changed it to abstract as it stays encapsulated.
# 2. I was passing allowed_spot_size as an argument in constructor. Made no sense as why will the uer input this?
# 2.1 So made it an abstract method and also made it a property, so as to it can't be called as it is only setting.
# 3. The abstractmethod forces every subclass to implement it.