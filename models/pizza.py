from datetime import datetime
from models.topping import Topping  # Přidání importu třídy Topping

class Pizza:
    def __init__(self, name, size, price):
        self.name = name
        self.size = size
        self.price = price
        self.toppings = []
        self.paid = False
        self.payment_method = None
        self.created_at = datetime.now()  # Přidání atributu pro datum a čas vytvoření objednávky
        self.completed_at = None  # Přidání atributu pro datum a čas vyřízení

    def add_topping(self, topping):
        self.toppings.append(topping)

    def get_total_price(self):
        total_price = self.price
        for topping in self.toppings:
            total_price += topping.price
        return total_price

    def to_dict(self):
        return {
            'name': self.name,
            'size': self.size,
            'price': self.price,
            'toppings': [topping.to_dict() for topping in self.toppings],
            'paid': self.paid,
            'payment_method': self.payment_method,
            'created_at': self.created_at.isoformat() if self.created_at else None,  # Uložení data a času vytvoření jako řetězec
            'completed_at': self.completed_at.isoformat() if self.completed_at else None  # Uložení data a času vyřízení jako řetězec
        }

    @classmethod
    def from_dict(cls, data):
        pizza = cls(data['name'], data['size'], data['price'])
        pizza.toppings = [Topping.from_dict(t) for t in data['toppings']]
        pizza.paid = data.get('paid', False)
        pizza.payment_method = data.get('payment_method', None)
        pizza.created_at = datetime.fromisoformat(data['created_at']) if data.get('created_at') else None  # Načtení data a času vytvoření z řetězce
        pizza.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None  # Načtení data a času vyřízení z řetězce
        return pizza
