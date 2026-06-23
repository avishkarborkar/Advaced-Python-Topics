#Issues with this code:
#The Liskov Substitution Principle (LSP) states that objects of a superclass should be replaceable by objects of its subclasses without affecting the correctness of the program
# For example Paypal uses email adress instead of secrity code:

# class PaypalPaymentProcessor(PaymentProcessor):
#     def pay(self, order, security_code):
#         print("Processing paypal payment type")
#         print(f"Using email address: {security_code}")
#         order.status = "paid"

# We are violating the principle as in PaymentProcessor pay(), we have security code as parameter.

#Solution:
#1. Let's remove security_code from the abstract class PaymentProcessor and add an initializer in every subclass to accept the required parameters.


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


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order, security_code):
        pass


class DebitPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):
    def pay(self, order, security_code):
        print("Processing paypal payment type")
        print(f"Using security code: {security_code}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
processor = PaypalPaymentProcessor()
processor.pay(order, "hi@arjancodes.com")