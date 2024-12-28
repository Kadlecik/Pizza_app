class Sales:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Sales, cls).__new__(cls)
            cls._instance.sales = []
        return cls._instance

    def record_sale(self, order):
        self.sales.append(order)

    def get_total_sales(self):
        return sum(order.get_total_price() for order in self.sales)

class Sales:
    def __init__(self):
        self.total_sales = 0.0

    def record_sale(self, order):
        self.total_sales += order.get_total_price()

    def get_total_sales(self):
        return self.total_sales

    def to_dict(self):
        return {'total_sales': self.total_sales}

    @classmethod
    def from_dict(cls, data):
        sales = cls()
        sales.total_sales = data.get('total_sales', 0.0)
        return sales
