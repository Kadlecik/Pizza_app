import tkinter as tk
from tkinter import messagebox

class ConfirmPaymentDialog:
    def __init__(self, root, controller, order_index):
        self.root = root
        self.controller = controller
        self.order_index = order_index

        self.confirm_window = tk.Toplevel(self.root)
        self.confirm_window.title("Confirm Payment")
        self.confirm_window.geometry("300x150")

        tk.Label(self.confirm_window, text="Is the order paid?").pack(pady=20)
        tk.Button(self.confirm_window, text="Yes", command=self.mark_as_paid).pack(pady=5)
        tk.Button(self.confirm_window, text="No", command=self.confirm_window.destroy).pack(pady=5)

    def mark_as_paid(self):
        self.controller.order.items[self.order_index].mark_as_paid()
        self.controller.save_orders("orders.json")
        messagebox.showinfo("Payment Confirmed", "The order has been marked as paid.")
        self.confirm_window.destroy()
