# user_management_view.py

from user_manager import UserManager
import tkinter as tk
from tkinter import ttk, messagebox

class UserManagementView:
    def __init__(self, root):
        self.root = tk.Toplevel(root)  # Vytvoření nového Toplevel okna
        self.root.title("User Management")

        self.frame = ttk.Frame(self.root)
        self.frame.grid(row=0, column=0, padx=20, pady=20, sticky="nsew")

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

        self.label = ttk.Label(self.frame, text="User Management", font=('Helvetica', 16, 'bold'))
        self.label.grid(row=0, column=0, columnspan=2, pady=10)

        # Vytvoření widgetů pro správu uživatelů
        self.create_widgets()

    def create_widgets(self):
        self.username_label = ttk.Label(self.frame, text="Username:")
        self.username_label.grid(row=1, column=0, padx=5, pady=5)

        self.username_entry = ttk.Entry(self.frame)
        self.username_entry.grid(row=1, column=1, padx=5, pady=5)

        self.password_label = ttk.Label(self.frame, text="Password:")
        self.password_label.grid(row=2, column=0, padx=5, pady=5)

        self.password_entry = ttk.Entry(self.frame, show="*")
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)

        self.role_label = ttk.Label(self.frame, text="Role:")
        self.role_label.grid(row=3, column=0, padx=5, pady=5)

        self.role_entry = ttk.Entry(self.frame)
        self.role_entry.grid(row=3, column=1, padx=5, pady=5)

        self.add_user_button = ttk.Button(self.frame, text="Add User", command=self.add_user)
        self.add_user_button.grid(row=4, column=0, columnspan=2, pady=5)

        self.edit_user_button = ttk.Button(self.frame, text="Edit User", command=self.edit_user)
        self.edit_user_button.grid(row=5, column=0, columnspan=2, pady=5)

        self.delete_user_button = ttk.Button(self.frame, text="Delete User", command=self.delete_user)
        self.delete_user_button.grid(row=6, column=0, columnspan=2, pady=5)

        self.users_listbox = tk.Listbox(self.frame)
        self.users_listbox.grid(row=7, column=0, columnspan=2, pady=5)

        self.user_manager = UserManager()  # Inicializace UserManager
        self.load_users()

    def load_users(self):
        self.users_listbox.delete(0, tk.END)
        for user in self.user_manager.users:
            self.users_listbox.insert(tk.END, f"{user.username} - {user.role}")

    def add_user(self):
        username = self.username_entry.get()
        password = self.password_entry.get()
        role = self.role_entry.get()

        if username and password:
            self.user_manager.add_user(username, password, role)
            self.load_users()
            messagebox.showinfo("Success", "User added successfully")
        else:
            messagebox.showwarning("Input Error", "Username and password cannot be empty")

    def edit_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE).split(" - ")[0]
        new_password = self.password_entry.get()
        new_role = self.role_entry.get()

        if not new_password and not new_role:
            messagebox.showwarning("Input Error", "No changes specified")
            return

        if self.user_manager.edit_user(selected_user, new_password, new_role):
            self.load_users()
            messagebox.showinfo("Success", "User edited successfully")
        else:
            messagebox.showwarning("Error", "User not found")

    def delete_user(self):
        selected_user = self.users_listbox.get(tk.ACTIVE).split(" - ")[0]

        if selected_user:
            self.user_manager.delete_user(selected_user)
            self.load_users()
            messagebox.showinfo("Success", "User deleted successfully")
        else:
            messagebox.showwarning("Error", "No user selected")
