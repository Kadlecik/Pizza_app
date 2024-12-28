import tkinter as tk
from tkinter import ttk, messagebox
from models.pizza import Pizza
from models.topping import Topping
from add_topping_dialog import AddToppingDialog
from PIL import Image, ImageTk

class CreateOrderDialog:
    def __init__(self, root, controller, current_orders_view=None):
        self.root = root
        self.controller = controller
        self.current_orders_view = current_orders_view

        self.order_window = tk.Toplevel(self.root)
        self.order_window.title("Create Order")
        self.order_window.geometry("500x300")

        root_x = self.root.winfo_x()
        root_y = self.root.winfo_y()
        root_width = self.root.winfo_width()
        self.order_window.geometry(f"+{root_x + root_width + 10}+{root_y}")  # +10 pixelů mezera

        tk.Label(self.order_window, text="Pizza Name").grid(row=0, column=0)
        self.pizza_name = ttk.Combobox(self.order_window, values=["Margherita", "Pepperoni", "Hawaiian", "Veggie"])
        self.pizza_name.grid(row=0, column=1)
        self.pizza_name.bind("<<ComboboxSelected>>", self.show_pizza_image)

        tk.Label(self.order_window, text="Size").grid(row=1, column=0)
        self.pizza_size = ttk.Combobox(self.order_window, values=["Small", "Medium", "Large"])
        self.pizza_size.grid(row=1, column=1)
        self.pizza_size.bind("<<ComboboxSelected>>", self.set_price_based_on_size)

        tk.Label(self.order_window, text="Base Price").grid(row=2, column=0)
        self.pizza_price = tk.Entry(self.order_window)
        self.pizza_price.grid(row=2, column=1)

        tk.Button(self.order_window, text="Add Topping", command=self.add_topping).grid(row=3, column=0, columnspan=2)
        tk.Button(self.order_window, text="Create", command=self.create_pizza).grid(row=4, column=0, columnspan=2)

        self.pizza_image_label = tk.Label(self.order_window)
        self.pizza_image_label.grid(row=0, column=2, rowspan=5, padx=10, pady=10)

        tk.Button(self.order_window, text="Close", command=self.order_window.destroy).grid(row=5, column=0, columnspan=2)

    def show_pizza_image(self, event):
        pizza_name = self.pizza_name.get().lower()
        image_path = f"images/pizza_{pizza_name}.jpg"
        try:
            image = Image.open(image_path)
            image = image.resize((200, 200), Image.Resampling.LANCZOS)
            photo = ImageTk.PhotoImage(image)
            self.pizza_image_label.config(image=photo)
            self.pizza_image_label.image = photo
        except Exception as e:
            messagebox.showerror("Image Error", f"Could not load image for {pizza_name}: {e}")

    def set_price_based_on_size(self, event):
        size = self.pizza_size.get()
        if size == "Small":
            price = 5.0
        elif size == "Medium":
            price = 8.0
        elif size == "Large":
            price = 12.0
        else:
            price = 0.0
        self.pizza_price.delete(0, tk.END)
        self.pizza_price.insert(0, f"{price:.2f}")

    def add_topping(self):
        AddToppingDialog(self.root, self.controller, self.current_orders_view, self.order_window)

    def create_pizza(self):
        name = self.pizza_name.get()
        size = self.pizza_size.get()
        price = float(self.pizza_price.get())
        if not name or not size or not price:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        pizza = Pizza(name, size, price)
        self.controller.order.add_pizza(pizza)
        self.controller.save_orders("orders.json")
        messagebox.showinfo("Pizza Created", f"Pizza {name} ({size}) with base price ${price} created.")
        if self.current_orders_view is not None:
            self.current_orders_view.update()
