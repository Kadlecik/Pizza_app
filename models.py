class Topping:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Pizza:
    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price
        self.toppings = []
        self.completed = False
        self.paid = False

    def add_topping(self, topping):
        self.toppings.append(topping)

    def get_total_price(self):
        total = self.price
        for topping in self.toppings:
            total += topping.price
        return total

    def mark_as_completed(self):
        self.completed = True

class Order:
    def __init__(self):
        self.items = []

    def add_pizza(self, pizza):
        self.items.append(pizza)
