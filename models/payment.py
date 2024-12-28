class CreditCardPayment:
    def pay(self, amount):
        print(f"Processing credit card payment for ${amount:.2f}")


class PayPalPayment:
    def pay(self, amount):
        print(f"Processing PayPal payment for ${amount:.2f}")


class CashPayment:
    def pay(self, amount):
        print(f"Processing cash payment for ${amount:.2f}")
