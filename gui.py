import ttkbootstrap as tb
import tkinter as tk
from tkinter import ttk, messagebox
from auth import authenticate, register_user
from logic import search_product, sell_product, add_product, view_sales_history


# Login Window
def open_login():
    login_window = tb.Window(themename="superhero")
    login_window.title("Cashier Login")
    login_window.state("zoomed")
    login_window.resizable(False, False)

    frame = tb.Frame(login_window, padding=30)
    frame.pack(expand=True)

    tb.Label(frame, text="🛒 Store Login", font=("Arial", 24, "bold")).pack(pady=20)

    tb.Label(frame, text="Username:", font=("Arial", 14)).pack(pady=5)
    username_entry = tb.Entry(frame, width=30, font=("Arial", 14))
    username_entry.pack(pady=5)

    tb.Label(frame, text="Password:", font=("Arial", 14)).pack(pady=5)
    password_entry = tb.Entry(frame, width=30, show="*", font=("Arial", 14))
    password_entry.pack(pady=5)

    def login():
        username = username_entry.get().strip()
        password = password_entry.get().strip()
        role = authenticate(username, password)

        if role:
            login_window.destroy()
            open_main_app(username, role)
        else:
            messagebox.showerror("Error", "Invalid username or password")

    tb.Button(frame, text="🔑 Login", bootstyle="success", command=login).pack(pady=10)

    login_window.mainloop()

# Main Application Window
def open_main_app(username, role):
    root = tb.Window(themename="superhero")
  
