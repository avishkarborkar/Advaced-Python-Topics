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

class SMSAuth(ABC):
    authorised = False
    def verify_sms_code(self, code):
        print(f"Verifying SMS code {code}")
        self.authorised = True

    def is_authorised(self) -> bool:
        return self.authorised


class PaymentProcessor(ABC):

    @abstractmethod
    def pay(self, order):
        pass

class DebitPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code, authorizer: SMSAuth):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorised():
            raise Exception("Not authorized")
        print("Processing debit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class CreditPaymentProcessor(PaymentProcessor):

    def __init__(self, security_code, authorizer: SMSAuth):
        self.security_code = security_code
        self.authorizer = authorizer

    def pay(self, order):
        if not self.authorizer.is_authorised():
            raise Exception("Not authorized")
        print("Processing credit payment type")
        print(f"Verifying security code: {self.security_code}")
        order.status = "paid"


class PaypalPaymentProcessor(PaymentProcessor):

    def __init__(self, email_address, authorizer: SMSAuth):
        self.email_address = email_address
        self.authorizer = authorizer

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

authorizer = SMSAuth()

print(order.total_price())
processor = DebitPaymentProcessor("2349875", authorizer)
authorizer.verify_sms_code(465839)
processor.pay(order)