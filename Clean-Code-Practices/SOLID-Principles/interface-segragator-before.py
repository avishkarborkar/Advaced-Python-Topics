#Issues with this code:
# The Interface Segregation Principle states that for a funcationality there must be specific interfaces rather than a general purpose interface.
# In this code, the PaymentProcessor interface has methods for both payment and SMS authorization. However, not all payment methods require SMS authorization (e.g., CreditPaymentProcessor).
# This forces classes that don't need SMS authorization to implement it, leading to unnecessary code and potential errors.

#Possible Pitfalls:
#1. CreditPaymentProcessor has to implement auth_sms method which it doesn't need, leading to confusion.
#2. If we want to add more payment methods that don't require SMS authorization, we would have to keep adding unnecessary methods to the PaymentProcessor interface.
#3. Testing becomes more complex as we have to test methods that are not relevant to certain payment processors.

#Solution:
#1. We create a subclass for PaymentProcessor and inherit its properties. e.g., PaymentProcessor_SMSMAUTH
#2. Simply make a new class to handle SMS AUthorisation
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
    def auth_sms(self, code):
        pass

    @abstractmethod
    def pay(self, order):
        pass


class DebitPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code):
        self.security_code = security_code
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code):
        self.security_code = security_code

    def auth_sms(self, code):
        raise Exception("Credit card payments don't support SMS code authorization.")

    def pay(self, order):
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):

    def __init__(self, email_address):
        self.email_address = email_address
        self.verified = False

    def auth_sms(self, code):
        print(f"Verifying SMS code {code}")
        self.verified = True

    def pay(self, order):
        if not self.verified:
            raise Exception("Not authorized")
        print("Processing paypal payment type")
        print(f"Using email address: {self.email_address}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
processor = DebitPaymentProcessor("2349875")
processor.auth_sms(465839)
processor.pay(order)