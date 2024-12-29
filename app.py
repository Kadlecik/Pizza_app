import sys
import os
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
import json
import logging

# Importování dalších potřebných modulů
from controllers.mainController import MainController
from current_orders_view import CurrentOrdersView
from completed_orders_view import CompletedOrdersView
from create_order_dialog import CreateOrderDialog
from process_payment_dialog import ProcessPaymentDialog
from models.order import Order
from models.pizza import Pizza
from models.sales import Sales
from login_dialog import LoginDialog
from user_management_view import UserManagementView
from user_manager import UserManager
from utils.plot_utils import plot_sales_data


# Načtení konfigurace
try:
    with open('config.json') as config_file:
        CONFIG = json.load(config_file)
except (FileNotFoundError, json.JSONDecodeError):
    CONFIG = {
        "orders_file": "orders.json",
        "completed_orders_file": "completed_orders.json",
        "sales_file": "sales.json",
        "users_file": "users.json"
    }

ORDERS_FILE = CONFIG['orders_file']
COMPLETED_ORDERS_FILE = CONFIG['completed_orders_file']
SALES_FILE = CONFIG['sales_file']
USERS_FILE = CONFIG['users_file']

# Nastavení logování
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class FileManager:
    @staticmethod
    def load_json(file_path, default=None):
        try:
            with open(file_path, 'r') as file:
                return json.load(file)
        except (FileNotFoundError, json.JSONDecodeError):
            return default or {}

    @staticmethod
    def save_json(file_path, data):
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=4)

class PizzaApp:
    def __init__(self, root, operator_name):
        self.root = root
        self.operator_name = operator_name
        self.root.title(f"Pizza Ordering System - Logged in as: {self.operator_name}")
        self.controller = MainController()
        self.user_management_window = None

        self.set_window_position()
        self.initialize_style()
        self.initialize_notebook()
        self.initialize_menu()

        # Načítání dat
        self.initialize_data()

    def set_window_position(self):
        window_width = 800
        window_height = 600
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.root.geometry(f'{window_width}x{window_height}+{x}+{y}')
        self.root.update_idletasks()

    def initialize_style(self):
        self.style = ttk.Style()
        self.style.configure('TNotebook', background='#f0f0f0', borderwidth=0)
        self.style.configure('TNotebook.Tab', font=('Helvetica', 10, 'bold'), padding=[10, 5])

    def initialize_notebook(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self.current_orders_frame = ttk.Frame(self.notebook)
        self.completed_orders_frame = ttk.Frame(self.notebook)
        self.user_management_frame = ttk.Frame(self.notebook)

        self.notebook.add(self.current_orders_frame, text='Current Orders')
        self.notebook.add(self.completed_orders_frame, text='Completed Orders')

        self.current_orders_view = CurrentOrdersView(self.current_orders_frame, self.controller)
        self.completed_orders_view = CompletedOrdersView(self.completed_orders_frame, self.controller)

    def initialize_menu(self):
        main_menu = tk.Menu(self.root)
        self.root.config(menu=main_menu)

        order_menu = tk.Menu(main_menu, tearoff=0)
        admin_menu = tk.Menu(main_menu, tearoff=0)

        main_menu.add_cascade(label="Order", menu=order_menu)
        main_menu.add_cascade(label="Admin", menu=admin_menu)

        self.create_menu(order_menu, [
            ("Create Order", self.create_order),
            ("View Orders", self.view_orders),
            ("Clear Orders", self.clear_orders),
            ("Process Payment", lambda: self.process_payment(None)),
            ("Exit", self.quit_app),
        ])

        self.create_menu(admin_menu, [
            ("View Sales", self.view_sales),
            ("Completed Orders Graph", self.completed_orders_view.view_sales_graph),  # Změna na view_sales_graph
            ("Orders Per Day Chart", self.completed_orders_view.view_orders_per_day_graph),
            ("Manage Users", self.manage_users),
        ])


        self.root.protocol("WM_DELETE_WINDOW", self.quit_app)

    def create_menu(self, menu, items):
        for label, command in items:
            menu.add_command(label=label, command=command)

    def initialize_data(self):
        from utils.parser import Parser
        self.controller.order = self.load_data(
            ORDERS_FILE,
            lambda x: Parser.json_to_order(json.dumps(x)) if isinstance(x, dict) else Parser.json_to_order(x),
            Order()
        )
        self.controller.completed_orders = self.load_data(
            COMPLETED_ORDERS_FILE,
            lambda x: [Pizza.from_dict(p) for p in x] if isinstance(x, list) else [],
            []
        )
        self.controller.sales = self.load_data(
            SALES_FILE,
            lambda x: Sales.from_dict(x) if isinstance(x, dict) else Sales(),
            Sales()
        )
        self.current_orders_view.update()
        self.completed_orders_view.update()

    def load_data(self, file_path, parser_method, default):
        data = FileManager.load_json(file_path, default)
        return parser_method(data)

    def create_order(self):
        CreateOrderDialog(self.root, self.controller, self.current_orders_view)

    def view_orders(self):
        self.notebook.select(self.current_orders_frame)
        self.current_orders_view.update()

    def clear_orders(self):
        self.controller.order = Order()
        FileManager.save_json(ORDERS_FILE, [])
        self.controller.save_orders(ORDERS_FILE)
        messagebox.showinfo("Clear Orders", "Order history cleared successfully.")
        self.current_orders_view.update()

    def view_sales(self):
        total_revenue = sum(
            pizza.price + sum(topping.price for topping in pizza.toppings)
            for pizza in self.controller.completed_orders
        )
        messagebox.showinfo("Total Sales", f"Total Revenue: ${total_revenue:.2f}")

    def process_payment(self, order_index):
        ProcessPaymentDialog(self.root, self.controller, order_index)

    def complete_order(self):
        if not self.controller.order.orders:
            messagebox.showwarning("Complete Order", "No orders to complete.")
            return

        completed_order = self.controller.order.orders.pop(0)  # Odeber první objednávku
        completed_order.completed_at = datetime.now()
        self.controller.completed_orders.append(completed_order)

        # Debug logy
        logging.info(f"Completed order: {completed_order.to_dict()}")

        FileManager.save_json(ORDERS_FILE, [order.to_dict() for order in self.controller.order.orders])
        FileManager.save_json(COMPLETED_ORDERS_FILE, [order.to_dict() for order in self.controller.completed_orders])

        # Debug: Kontrola uložených dat
        logging.info(f"Updated current orders: {FileManager.load_json(ORDERS_FILE)}")
        logging.info(f"Updated completed orders: {FileManager.load_json(COMPLETED_ORDERS_FILE)}")

        self.current_orders_view.update()
        self.completed_orders_view.update()

        messagebox.showinfo("Complete Order", "Order has been completed and moved to Completed Orders.")

    def manage_users(self):
        if self.user_management_window is None or not self.user_management_window.winfo_exists():
            self.user_management_window = UserManagementView(self.root)
        else:
            self.user_management_window.lift()

    def quit_app(self):
        self.controller.save_orders(ORDERS_FILE)
        self.controller.save_completed_orders(COMPLETED_ORDERS_FILE)
        self.controller.save_sales(SALES_FILE)
        self.root.quit()

    def authenticate_user(self, username, password):
        logging.info(f"Authenticating user: {username}")
        user_manager = UserManager()
        if user_manager.validate_user(username, password):
            logging.info("Login successful.")
            return True
        else:
            logging.warning("Login failed.")
            return False

def main():
    root = tk.Tk()

    def on_login_success(username):
        root.deiconify()
        app = PizzaApp(root, username)
        app.set_window_position()

    def authenticate(username, password):
        logging.info(f"Login attempt with username: {username}")
        user_manager = UserManager()
        if user_manager.validate_user(username, password):
            on_login_success(username)
        else:
            messagebox.showerror("Login Failed", "Invalid username or password")

    login_dialog = LoginDialog(root, authenticate)
    root.withdraw()
    login_dialog.grab_set()
    root.mainloop()


def view_sales_graph(self):
    sales_data = [
        pizza.price + sum(topping.price for topping in pizza.toppings)
        for pizza in self.controller.completed_orders
    ]
    plot_sales_data(sales_data)



if __name__ == "__main__":
    main()
