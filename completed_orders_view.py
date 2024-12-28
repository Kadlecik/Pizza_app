import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import logging
from collections import Counter
from utils.fileManager import FileManager  # Import FileManager pro ukládání JSON
from models.pizza import Pizza  # Import třídy Pizza
from utils.plot_utils import plot_sales_data  # Import funkce pro graf
import matplotlib.pyplot as plt  # Import Matplotlib pro vykreslení grafů

COMPLETED_ORDERS_FILE = "completed_orders.json"

class CompletedOrdersView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.completed_orders_frame = ttk.Frame(self.root)
        self.completed_orders_frame.pack(fill=tk.BOTH, expand=True)

        # Přidání posuvníku
        self.canvas = tk.Canvas(self.completed_orders_frame)
        self.scrollbar = ttk.Scrollbar(self.completed_orders_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = ttk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        self.update()

    def update(self):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        total_price = 0.0

        # Přidání celkové ceny na začátek
        total_frame = ttk.Frame(self.scrollable_frame, padding="10 10 10 10", relief=tk.RIDGE, borderwidth=2)
        total_frame.pack(fill=tk.X, pady=10)

        for pizza in self.controller.completed_orders:
            total_price += pizza.price + sum(topping.price for topping in pizza.toppings)

        tk.Label(total_frame, text=f"Total Revenue: ${total_price:.2f}", font=('Helvetica', 12, 'bold'), anchor="w").pack(fill=tk.X)

        for idx, pizza in enumerate(self.controller.completed_orders):
            try:
                order_frame = ttk.Frame(self.scrollable_frame, padding="10 10 10 10", relief=tk.RIDGE, borderwidth=2)
                order_frame.pack(fill=tk.X, pady=10)

                created_at = pizza.completed_at.strftime('%Y-%m-%d %H:%M:%S') if pizza.completed_at else "Unknown"
                payment_method = pizza.payment_method if pizza.payment_method else "Unknown"

                tk.Label(order_frame, text=f"Order {idx + 1}", font=('Helvetica', 10, 'bold'), anchor="w").pack(fill=tk.X)
                tk.Label(order_frame, text=f"Completed At: {created_at}", anchor="w").pack(fill=tk.X)
                tk.Label(order_frame, text=f"Pizza: {pizza.name} - ${pizza.price}", font=('Helvetica', 10, 'bold'), anchor="w").pack(fill=tk.X)

                for topping in pizza.toppings:
                    tk.Label(order_frame, text=f"Topping: {topping.name} - ${topping.price}", anchor="w").pack(fill=tk.X)

                tk.Label(order_frame, text=f"Payment Method: {payment_method}", anchor="w").pack(fill=tk.X)
            except AttributeError as e:
                logging.error(f"Error displaying completed order {idx}: {e}")

    def pay_order(self, index, method):
        try:
            pizza = self.controller.completed_orders[index]
            pizza.paid = True
            pizza.payment_method = method
            FileManager.save_json(COMPLETED_ORDERS_FILE, [order.to_dict() for order in self.controller.completed_orders])
            messagebox.showinfo("Payment Confirmed", f"Payment for {pizza.name} has been confirmed via {method}.")
        except IndexError as e:
            logging.error(f"Invalid order index: {e}")
            messagebox.showerror("Error", "Invalid order selected.")
        except Exception as e:
            logging.error(f"Error processing payment: {e}")
            messagebox.showerror("Error", "An error occurred while processing the payment.")

    def view_sales_graph(self):
        sales_data = [
            pizza.price + sum(topping.price for topping in pizza.toppings)
            for pizza in self.controller.completed_orders
        ]
        logging.info(f"Sales data for graph: {sales_data}")
        plot_sales_data(sales_data)

    def view_orders_per_day_graph(self):
        # Výpočet počtu objednávek za den
        orders_by_date = Counter(
            pizza.completed_at.date() if pizza.completed_at else "Unknown"
            for pizza in self.controller.completed_orders
        )

        # Příprava dat pro graf
        dates = list(orders_by_date.keys())
        order_counts = list(orders_by_date.values())

        # Vykreslení grafu
        plt.bar(dates, order_counts)
        plt.title("Orders Per Day")
        plt.xlabel("Date")
        plt.ylabel("Number of Orders")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()
