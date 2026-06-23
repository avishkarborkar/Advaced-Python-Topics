import abc
from abc import ABC, abstractmethod

class Order:

    def __init__(self):
        self.items = []
        self.quantities = []
        self.prices = []
        self.status = "open"

    def add_item(self, name, quantity, price):
        self.items.append(name)
        self.quantities.append(quantity)
        self.prices.append(price)

    def total_price(self):
        total = 0
        for i in range(len(self.prices)):
            total += self.quantities[i] * self.prices[i]
        return total

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, order, security_code):
        pass

class DebitPaymentProcessor(PaymentMethod):
    def pay(self, order, security_code):
        print("Processing debit payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

class CreditPaymentProcessor(PaymentMethod):
    def pay(self, order, security_code):
        print("Processing credit payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

class PaypalPaymentProcessor(PaymentMethod):
    def pay(self, order, security_code):
        print("Processing Paypal payment")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(f"Total price: {order.total_price()}")
#processor = DebitPaymentProcessor()
processor = PaypalPaymentProcessor()
processor.pay(order, "0372846")