class Topping:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def to_dict(self):
        return {
            'name': self.name,
            'price': self.price
        }

    @classmethod
    def from_dict(cls, data):
        return cls(data['name'], data['price'])
