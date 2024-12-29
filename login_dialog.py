import tkinter as tk
from tkinter import messagebox


class LoginDialog(tk.Toplevel):  # Dědí od Toplevel pro modální okno
    def __init__(self, parent, authenticate_callback):
        super().__init__(parent)  # Volání konstruktoru Toplevel
        self.authenticate_callback = authenticate_callback

        self.title("Login")
        self.geometry("300x200")  # Nastavíme vhodnou velikost okna
        self.resizable(False, False)  # Zakážeme změnu velikosti okna

        # Vytvoření uživatelského jména a hesla
        self.username_label = tk.Label(self, text="Username:")
        self.username_label.pack(pady=5)  # Patří k vertikálnímu rozestupu mezi widgety

        self.username_entry = tk.Entry(self)
        self.username_entry.pack(pady=5)

        self.password_label = tk.Label(self, text="Password:")
        self.password_label.pack(pady=5)

        self.password_entry = tk.Entry(self, show="*")  # Heslo bude skrytě zobrazeno
        self.password_entry.pack(pady=5)

        # Tlačítko pro přihlášení
        self.login_button = tk.Button(self, text="Login", command=self.authenticate)
        self.login_button.pack(pady=10)

        # Zajištění, že přihlašovací okno bude modální (neumožní interakci s hlavním oknem)
        self.grab_set()  # Zablokuje interakci s hlavním oknem
        self.focus_set()  # Ujistí se, že toto okno je aktivní

    def authenticate(self):
        # Získáme uživatelské jméno a heslo
        username = self.username_entry.get()
        password = self.password_entry.get()

        # Zavoláme zpětnou funkci pro autentizaci
        self.authenticate_callback(username, password)
        self.destroy()  # Zavření okna po úspěšném přihlášení
