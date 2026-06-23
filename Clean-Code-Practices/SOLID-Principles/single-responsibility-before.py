#Issues with this code:
# Single-Responsibility Principle states that a function should have high coeheison, meaning it should focus on a single task or responsibility.
# In this code the class Orden is doing multiple tasks, such as managing order items, calculating total price, and processing payments.

#Possible Pitfalls:
# 1. Class order had both Payment Processing and Order Management responsibilities.
# 2. If we need to change the payment processing logic, we would have to modify the Order class, which could introduce bugs in order management.
# 3. Testing becomes more complex as we have to test both order management and payment processing in the same class.
# 4. The code is less reusable, as the payment processing logic is tightly coupled with the Order class.

#Solution:
#1. Separate the payment processing logic into its own class, PaymentProcessor.

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

    def pay(self, payment_type, security_code):
        if payment_type == "debit":
            print("Processing debit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        elif payment_type == "credit":
            print("Processing credit payment type")
            print(f"Verifying security code: {security_code}")
            self.status = "paid"
        else:
            raise Exception(f"Unknown payment type: {payment_type}")


order = Order()
order.add_item("Keyboard", 1, 50)
order.add_item("SSD", 1, 150)
order.add_item("USB cable", 2, 5)

print(order.total_price())
order.pay("debit", "0372846")
