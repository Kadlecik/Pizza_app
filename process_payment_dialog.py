import tkinter as tk
from confirm_payment_dialog import ConfirmPaymentDialog

class ProcessPaymentDialog:
    def __init__(self, root, controller, order_index):
        self.root = root
        self.controller = controller
        self.order_index = order_index

        self.payment_window = tk.Toplevel(self.root)
        self.payment_window.title("Process Payment")
        self.payment_window.geometry("300x200")

        tk.Label(self.payment_window, text="Choose Payment Method").pack(pady=20)
        tk.Button(self.payment_window, text="Credit Card", command=self.process_credit_card).pack(pady=10)
        tk.Button(self.payment_window, text="PayPal", command=self.process_paypal).pack(pady=10)
        tk.Button(self.payment_window, text="Cash", command=self.process_cash).pack(pady=10)  # Přidání tlačítka Cash
        tk.Button(self.payment_window, text="Cancel", command=self.payment_window.destroy).pack(pady=10)

    def process_credit_card(self):
        ConfirmPaymentDialog(self.root, self.controller, self.order_index)
        self.controller.current_orders_view.update()  # Aktualizace zobrazení po platbě
        self.payment_window.destroy()  # Zavření okna po platbě

    def process_paypal(self):
        ConfirmPaymentDialog(self.root, self.controller, self.order_index)
        self.controller.current_orders_view.update()  # Aktualizace zobrazení po platbě
        self.payment_window.destroy()  # Zavření okna po platbě

    def process_cash(self):  # Přidání metody pro hotovostní platbu
        ConfirmPaymentDialog(self.root, self.controller, self.order_index)
        self.controller.current_orders_view.update()  # Aktualizace zobrazení po platbě
        self.payment_window.destroy()  # Zavření okna po platbě
