import matplotlib.pyplot as plt
from notifications import send_email
from models.order import Order
from models.pizza import Pizza
from models.sales import Sales
from tkinter import ttk, messagebox
import json
from datetime import datetime

class MainController:
    def __init__(self):
        self.order = Order()
        self.completed_orders = []
        self.sales = Sales()

    def update_total_price(self, total_price_label):
        total_price = sum(pizza.price + sum(topping.price for topping in pizza.toppings) for pizza in self.order.items)
        total_price_label.config(text=f"Total Price: ${total_price:.2f}")

    def complete_order(self, index, total_price_label):
        pizza = self.order.items[index]
        if not pizza.paid:
            messagebox.showwarning("Payment Warning", "The order is not marked as paid. Please confirm the payment before completing the order.")
            return
        pizza.completed_at = datetime.now()
        self.order.items.pop(index)
        self.completed_orders.append(pizza)
        self.save_orders("orders.json")
        self.save_completed_orders("completed_orders.json")
        self.update_total_price(total_price_label)
        messagebox.showinfo("Order Completed", f"Order for {pizza.name} has been completed.")
        self.notify_order_completed(pizza)

    def save_orders(self, filename="orders.json"):
        with open(filename, 'w') as file:
            json.dump(self.order.to_dict(), file)

    def load_orders(self, filename="orders.json"):
        try:
            with open(filename, 'r') as file:
                self.order = Order.from_dict(json.load(file))
        except FileNotFoundError:
            self.order = Order()

    def save_completed_orders(self, filename="completed_orders.json"):
        with open(filename, 'w') as file:
            json.dump([order.to_dict() for order in self.completed_orders], file)

    def load_completed_orders(self, filename="completed_orders.json"):
        try:
            with open(filename, 'r') as file:
                self.completed_orders = [Order.from_dict(data) for data in json.load(file)]
        except FileNotFoundError:
            self.completed_orders = []

    def save_sales(self, filename="sales.json"):
        with open(filename, 'w') as file:
            json.dump(self.sales.to_dict(), file)

    def load_sales(self, filename="sales.json"):
        try:
            with open(filename, 'r') as file:
                self.sales = Sales.from_dict(json.load(file))
        except FileNotFoundError:
            self.sales = Sales()

    def process_payment(self, order_index, total_price_label):
        ProcessPaymentDialog(self.ui.root, self.controller, order_index)
        pizza = self.order.items[order_index]
        pizza.paid = True
        self.save_orders("orders.json")
        self.update_total_price(total_price_label)
        self.notify_payment_received(pizza)

    def quit_app(self):
        self.save_orders("orders.json")
        self.save_completed_orders("completed_orders.json")
        self.save_sales("sales.json")
        self.ui.root.quit()

    def notify_new_order(self, order):
        subject = "New Order Notification"
        body = f"A new order has been placed:\n\n{order}"
        to_email = "user@example.com"
        send_email(subject, body, to_email)

    def notify_payment_received(self, order):
        subject = "Payment Received Notification"
        body = f"Payment has been received for the following order:\n\n{order}"
        to_email = "user@example.com"
        send_email(subject, body, to_email)

    def notify_order_completed(self, order):
        subject = "Order Completed Notification"
        body = f"The following order has been completed:\n\n{order}"
        to_email = "user@example.com"
        send_email(subject, body, to_email)

    def plot_sales(self):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        sales = [100, 150, 200, 130, 170, 250, 300]

        plt.figure(figsize=(10, 5))
        plt.plot(days, sales, marker='o', linestyle='-', color='b')
        plt.title("Weekly Sales")
        plt.xlabel("Days")
        plt.ylabel("Sales ($)")
        plt.grid(True)
        plt.show()

    def plot_orders(self):
        days = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
        orders = [10, 20, 15, 10, 25, 30, 35]

        plt.figure(figsize=(10, 5))
        plt.bar(days, orders, color='g')
        plt.title("Weekly Orders")
        plt.xlabel("Days")
        plt.ylabel("Number of Orders")
        plt.grid(True)
        plt.show()
