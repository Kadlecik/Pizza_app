import tkinter as tk
from tkinter import ttk

class ViewOrdersDialog:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        orders_window = tk.Toplevel(self.root)
        orders_window.title("Current Orders")
        orders_window.geometry("+700+100")
        orders_text = tk.Text(orders_window)
        orders_text.pack()

        for i, pizza in enumerate(self.controller.order.items, start=1):
            pizza_info = f"Pizza {i}: {pizza.name} - {pizza.size} - ${pizza.get_total_price()}\n"
            toppings_info = "\n".join([f"  Topping: {topping.name} - ${topping.price}" for topping in pizza.toppings])
            orders_text.insert(tk.END, pizza_info + "\n" + toppings_info + "\n\n")
