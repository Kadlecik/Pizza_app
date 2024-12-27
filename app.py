class Pizza:
    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price
        self.toppings = []

    def add_topping(self, topping):
        self.toppings.append(topping)

    def get_total_price(self):
        return self.price + sum(topping.price for topping in self.toppings)

    def __str__(self):
        return f"Pizza: {self.name}, Size: {self.size}, Price: {self.get_total_price()}, Toppings: {[str(t) for t in self.toppings]}"
