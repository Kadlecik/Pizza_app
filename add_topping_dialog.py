import tkinter as tk
from tkinter import ttk, messagebox
from models.topping import Topping
from PIL import Image, ImageTk

# Seznam dostupných toppingů
AVAILABLE_TOPPINGS = [
    {"name": "Pepperoni", "price": 1.5, "image": "images/topping_pepperoni.jpg"},
    {"name": "Mushrooms", "price": 1.0, "image": "images/topping_mushrooms.jpg"},
    {"name": "Onions", "price": 0.5, "image": "images/topping_onions.jpg"},
    {"name": "Sausage", "price": 1.8, "image": "images/topping_sausage.jpg"},
    {"name": "Bacon", "price": 1.6, "image": "images/topping_bacon.jpg"},
    {"name": "Olives", "price": 1.2, "image": "images/topping_olives.jpg"},
    {"name": "Green Peppers", "price": 1.0, "image": "images/topping_green_peppers.jpg"},
    {"name": "Pineapple", "price": 1.3, "image": "images/topping_pineapple.jpg"},
    {"name": "Spinach", "price": 1.1, "image": "images/topping_spinach.jpg"},
    {"name": "Tomatoes", "price": 1.0, "image": "images/topping_tomatoes.jpg"}
]

class AddToppingDialog:
    def __init__(self, root, controller, current_orders_view=None, create_order_window=None):
        self.root = root
        self.controller = controller
        self.current_orders_view = current_orders_view

        self.topping_window = tk.Toplevel(self.root)
        self.topping_window.title("Add Topping")
        self.topping_window.geometry("400x300")

        # Nastavení pozice okna Add Topping
        root_x = create_order_window.winfo_x()
        root_y = create_order_window.winfo_y()
        root_height = create_order_window.winfo_height()
        self.topping_window.geometry(f"+{root_x}+{root_y + root_height + 10}")  # +10 pixelů mezera

        tk.Label(self.topping_window, text="Select Topping").grid(row=0, column=0)
        self.topping_combobox = ttk.Combobox(self.topping_window, values=[topping["name"] for topping in AVAILABLE_TOPPINGS])
        self.topping_combobox.grid(row=0, column=1)
        self.topping_combobox.bind("<<ComboboxSelected>>", self.show_topping_image)

        tk.Label(self.topping_window, text="Quantity").grid(row=1, column=0)
        self.topping_quantity = ttk.Combobox(self.topping_window, values=[1, 2, 3, 4, 5])  # Přidání rozbalovacího menu pro množství
        self.topping_quantity.grid(row=1, column=1)

        tk.Label(self.topping_window, text="Topping Price").grid(row=2, column=0)
        self.topping_price = tk.Entry(self.topping_window)
        self.topping_price.grid(row=2, column=1)

        self.topping_image_label = tk.Label(self.topping_window)
        self.topping_image_label.grid(row=0, column=2, rowspan=3, padx=10, pady=10)

        tk.Button(self.topping_window, text="Add", command=self.add_topping_to_order).grid(row=3, column=0, columnspan=2)
        tk.Button(self.topping_window, text="Close", command=self.topping_window.destroy).grid(row=4, column=0, columnspan=2)

    def show_topping_image(self, event):
        topping_name = self.topping_combobox.get()
        selected_topping = next((topping for topping in AVAILABLE_TOPPINGS if topping["name"] == topping_name), None)
        if selected_topping:
            image_path = selected_topping["image"]
            try:
                image = Image.open(image_path)
                image = image.resize((100, 100), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(image)
                self.topping_image_label.config(image=photo)
                self.topping_image_label.image = photo
                self.topping_price.delete(0, tk.END)
                self.topping_price.insert(0, f"{selected_topping['price']:.2f}")
            except Exception as e:
                messagebox.showerror("Image Error", f"Could not load image for {topping_name}: {e}")

    def add_topping_to_order(self):
        name = self.topping_combobox.get()
        price = float(self.topping_price.get())
        quantity = int(self.topping_quantity.get())
        if not name or not price or not quantity:
            messagebox.showwarning("Warning", "Please fill in all fields.")
            return
        topping = Topping(name, price * quantity)
        selected_pizza = self.controller.order.items[-1]  # Předpokládáme, že přidáváme toping k poslední vytvořené pizze
        selected_pizza.add_topping(topping)
        self.controller.save_orders("orders.json")
        messagebox.showinfo("Topping Added", f"{quantity}x {name} topping(s) added.")
        if self.current_orders_view is not None:
            self.current_orders_view.update()
        self.topping_window.destroy()
