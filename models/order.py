from models.pizza import Pizza  # Přidání importu třídy Pizza
from datetime import datetime

class Order:
    def __init__(self):
        self.items = []
        self.created_at = datetime.now()  # Přidání atributu pro datum a čas
        self.completed_at = None  # Přidání atributu pro datum a čas vyřízení

    def to_dict(self):
        return {
            'items': [item.to_dict() for item in self.items],
            'created_at': self.created_at.isoformat(),  # Uložení data a času jako řetězec
            'completed_at': self.completed_at.isoformat() if self.completed_at else None  # Uložení data a času vyřízení jako řetězec
        }

    @classmethod
    def from_dict(cls, data):
        order = cls()
        order.items = [Pizza.from_dict(item) for item in data['items']]
        order.created_at = datetime.fromisoformat(data.get('created_at', datetime.now().isoformat()))  # Načtení data a času z řetězce
        order.completed_at = datetime.fromisoformat(data['completed_at']) if data.get('completed_at') else None  # Načtení data a času vyřízení z řetězce
        return order

    def add_pizza(self, pizza):
        self.items.append(pizza)

    def get_total_price(self):
        total_price = 0.0
        for pizza in self.items:
            total_price += pizza.get_total_price()
        return total_price
