from models import Order, Pizza, Topping


class MainController:
    def __init__(self):
        self.order = Order()
        self.pizzas = {
            "Margherita": ["Tomato", "Mozzarella", "Basil"],
            "Pepperoni": ["Tomato", "Mozzarella", "Pepperoni"],
            "Hawaiian": ["Tomato", "Mozzarella", "Ham", "Pineapple"],
            "Vegetarian": ["Tomato", "Mozzarella", "Bell Peppers", "Olives", "Mushrooms"],
            "BBQ Chicken": ["BBQ Sauce", "Mozzarella", "Chicken", "Red Onions", "Cilantro"],
            "Meat Lovers": ["Tomato", "Mozzarella", "Pepperoni", "Sausage", "Ham", "Bacon"],
            "Four Cheese": ["Tomato", "Mozzarella", "Cheddar", "Parmesan", "Gorgonzola"],
            "Seafood": ["Tomato", "Mozzarella", "Shrimp", "Calamari", "Mussels"],
            "Mexican": ["Tomato", "Mozzarella", "Ground Beef", "Jalapenos", "Sour Cream"],
            "Buffalo Chicken": ["Buffalo Sauce", "Mozzarella", "Chicken", "Celery", "Blue Cheese"]
        }

    def save_orders(self, filename):
        # Implementace uložení objednávek do souboru
        pass

    def load_orders(self, filename):
        # Implementace načtení objednávek ze souboru
        pass
from datetime import datetime

class Pizza:
    def __init__(self, name, price, toppings=None):
        self.name = name
        self.price = price
        self.toppings = toppings if toppings else []
        self.paid = False
        self.payment_method = None

class Order:
    def __init__(self):
        self.items = []
        self.created_at = datetime.now()

class Controller:
    def __init__(self):
        self.order = Order()
        self.completed_orders = []

    def save_orders(self, filename):
        pass  # Dummy method for testing

    def save_completed_orders(self, filename):
        pass  # Dummy method for testing
