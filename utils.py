import json
import os
from models import Pizza, Topping, Order

class Parser:
    @staticmethod
    def order_to_json(order):
        return json.dumps({
            "items": [
                {
                    "name": pizza.name,
                    "size": pizza.size,
                    "price": pizza.price,
                    "toppings": [{"name": topping.name, "price": topping.price} for topping in pizza.toppings],
                    "paid": pizza.paid,
                    "completed": pizza.completed
                } for pizza in order.items
            ]
        }, indent=4)

    @staticmethod
    def json_to_order(order_json):
        order_data = json.loads(order_json)
        order = Order()
        for pizza_data in order_data["items"]:
            pizza = Pizza(pizza_data["name"], pizza_data["size"], pizza_data["price"])
            for topping_data in pizza_data["toppings"]:
                topping = Topping(topping_data["name"], topping_data["price"])
                pizza.add_topping(topping)
            pizza.paid = pizza_data.get("paid", False)
            pizza.completed = pizza_data.get("completed", False)  # Přidání defaultní hodnoty
            order.add_pizza(pizza)
        return order

class FileManager:
    @staticmethod
    def save_to_file(data, filename):
        with open(filename, 'w') as file:
            file.write(data)

    @staticmethod
    def read_from_file(filename):
        if not os.path.exists(filename):
            return None
        with open(filename, 'r') as file:
            return file.read()
