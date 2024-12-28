import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from receipt_generator import create_receipt

class CurrentOrdersView:
    def __init__(self, root, controller):
        self.root = root
        self.controller = controller

        self.orders_frame = ttk.Frame(self.root)
        self.orders_frame.pack(fill=tk.BOTH, expand=True)

        # Přidání posuvníku
        self.canvas = tk.Canvas(self.orders_frame)
        self.scrollbar = ttk.Scrollbar(self.orders_frame, orient="vertical", command=self.canvas.yview)
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

        self.total_price_window = None
        print("Initial call to update from __init__")  # Ladicí zpráva
        self.update()

    def calculate_total_price(self):
        total_price = 0
        for pizza in self.controller.order.items:
            total_price += pizza.price
            for topping in pizza.toppings:
                total_price += topping.price
        return total_price

    def show_total_price(self):
        total_price = self.calculate_total_price()
        if self.total_price_window is None or not self.total_price_window.winfo_exists():
            self.total_price_window = tk.Toplevel(self.root)
            self.total_price_window.title("Total Price")
            self.total_price_window.geometry("300x100")

            self.total_price_label = tk.Label(self.total_price_window, text=f"Total Price: ${total_price:.2f}", font=('Helvetica', 12, 'bold'), anchor="center")
            self.total_price_label.pack(fill=tk.BOTH, expand=True, pady=20)
        else:
            self.total_price_label.config(text=f"Total Price: ${total_price:.2f}")
        self.total_price_window.deiconify()  # Ujistíme se, že okno je zobrazeno

    def update(self):
        print("Updating orders...")  # Ladicí zpráva
        # Odstranění všech widgetů
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()
            print("Widget removed")  # Ladicí zpráva

        for idx, pizza in enumerate(self.controller.order.items):
            print(f"Displaying order {idx + 1}")  # Ladicí zpráva
            # Vytvoření rámce pro objednávku
            order_frame = ttk.Frame(self.scrollable_frame, padding="10 10 10 10", relief=tk.RIDGE, borderwidth=2)
            order_frame.pack(fill=tk.X, pady=10)

            payment_method = pizza.payment_method if hasattr(pizza, 'payment_method') else "Unpaid"
            created_at = self.controller.order.created_at.strftime('%Y-%m-%d %H:%M:%S')

            order_label = tk.Label(order_frame, text=f"Order {idx + 1}", font=('Helvetica', 10, 'bold'), anchor="w")
            order_label.pack(fill=tk.X)

            created_at_label = tk.Label(order_frame, text=f"Created At: {created_at}", anchor="w")
            created_at_label.pack(fill=tk.X)

            pizza_label = tk.Label(order_frame, text=f"Pizza: {pizza.name} - ${pizza.price}",
                                   font=('Helvetica', 10, 'bold'), anchor="w")
            pizza_label.pack(fill=tk.X)

            for topping in pizza.toppings:
                topping_label = tk.Label(order_frame, text=f"Topping: {topping.name} - ${round(topping.price, 1)}",
                                         font=('Helvetica', 10, 'bold'), anchor="w")
                topping_label.pack(fill=tk.X)

            # Přidání oddělovací čáry před Total Price
            separator = ttk.Separator(order_frame, orient="horizontal")
            separator.pack(fill=tk.X, pady=5)

            # Výpočet celkové ceny objednávky
            total_price = pizza.price + sum(topping.price for topping in pizza.toppings)
            total_price_label = tk.Label(order_frame, text=f"Total Order Price: ${total_price:.2f}",
                                         font=('Helvetica', 10, 'bold'), anchor="w")
            total_price_label.pack(fill=tk.X)

            payment_status = "Paid" if pizza.paid else "Unpaid"
            payment_status_label = tk.Label(order_frame, text=f"{payment_status}",
                                            font=('Helvetica', 10, 'bold' if pizza.paid else 'normal'), anchor="w")
            payment_status_label.pack(fill=tk.X)

            payment_method_label = tk.Label(order_frame, text=f"Payment Method: {payment_method}", anchor="w")
            payment_method_label.pack(fill=tk.X)

            action_frame = ttk.Frame(order_frame)
            action_frame.pack(anchor=tk.W, pady=5)

            pay_button = tk.Button(action_frame, text="Pay", command=lambda idx=idx: self.open_payment_dialog(idx))
            pay_button.pack(side=tk.LEFT, padx=5)

            close_button = tk.Button(action_frame, text="Close Order", command=lambda idx=idx: self.close_order(idx))
            close_button.pack(side=tk.LEFT, padx=5)
        print("Orders updated")  # Ladicí zpráva

    def add_order(self, pizza):
        print(f"Adding order for {pizza.name}")  # Ladicí zpráva
        self.controller.order.items.append(pizza)
        self.controller.save_orders("orders.json")
        self.update()
        self.show_total_price()  # Otevření okna s celkovou cenou při vytvoření nové objednávky

    def open_payment_dialog(self, index):
        self.payment_dialog = tk.Toplevel(self.root)
        self.payment_dialog.title("Select Payment Method")
        self.payment_dialog.geometry("300x200")

        payment_methods = ["Credit Card", "PayPal", "Cash"]
        tk.Label(self.payment_dialog, text="Select Payment Method:").pack(pady=10)
        for method in payment_methods:
            button = tk.Button(self.payment_dialog, text=method, command=lambda method=method: self.pay_order(index, method))
            button.pack(pady=5)

    def close_order(self, index):
        print(f"Closing order {index}")  # Ladicí zpráva
        pizza = self.controller.order.items[index]
        if not pizza.paid:
            messagebox.showwarning("Payment Warning", "The order is not marked as paid. Please confirm the payment before completing the order.")
            return
        pizza.completed_at = datetime.now()  # Uložení data a času vyřízení objednávky
        self.controller.order.items.pop(index)  # Odebrání ukončené objednávky ze seznamu
        self.controller.completed_orders.append(pizza)
        self.controller.save_orders("orders.json")
        self.controller.save_completed_orders("completed_orders.json")
        self.update()  # Aktualizace zobrazení objednávek
        messagebox.showinfo("Order Completed", f"Order for {pizza.name} has been completed.")
        print("Order closed and update called")  # Ladicí zpráva

    def pay_order(self, index, method):
        print(f"Paying for order {index} with method {method}")  # Ladicí zpráva
        pizza = self.controller.order.items[index]
        pizza.paid = True
        pizza.payment_method = method  # Uložení způsobu platby do objektu pizza
        self.controller.save_orders("orders.json")
        self.payment_dialog.destroy()
        self.update()
        create_receipt(pizza)  # Vytvoření účtenky
        messagebox.showinfo("Payment Confirmed", f"Payment for {pizza.name} has been confirmed via {method}.")
