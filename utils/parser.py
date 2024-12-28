import json
from models.order import Order
from models.pizza import Pizza
from models.topping import Topping

class Parser:
    @staticmethod
    def json_to_order(json_data):
        order_dict = json.loads(json_data)
        return Order.from_dict(order_dict)

    @staticmethod
    def order_to_json(order):
        return json.dumps(order.to_dict())
