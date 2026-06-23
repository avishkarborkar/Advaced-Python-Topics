#Issues with this code:
# Open-Closed Principle states that software entities (classes, modules, functions, etc.) should be open for extension but closed for modification.
# In this code, if we want to add a new payment method, we would have to modify the existing PaymentProcessor class, which violates this principle.

#Possible Pitfalls:
#1. I want to add a new payment method (e.g., PayPal), I would have to modify the PaymentProcessor class, which could introduce bugs in existing payment methods.
#2. The PaymentProcessor class has multiple reasons to change (adding new payment methods), which violates the Single Responsibility Principle as well.
#3. Testing becomes more complex as we have to tesrt all payment methods in the same class.

#Solution:
#1. Create an abstract PaymentMethod class/interface that defines a pay method.
#2. Now we cna use the abstract class to create different payment methods.

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


class PaymentProcessor:
    def pay_debit(self, order, security_code):
        print("Processing debit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"

    def pay_credit(self, order, security_code):
        print("Processing credit payment type")
        print(f"Verifying security code: {security_code}")
        order.status = "paid"


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
processor = PaymentProcessor()
processor.pay_debit(order, "0372846")