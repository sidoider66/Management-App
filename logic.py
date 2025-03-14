import pandas as pd
from openpyxl import load_workbook
from datetime import datetime
import os
from auth import authenticate  # Avoid circular import

# Define file paths
products_file = r"D:\Doc\pyhton_projects\Gestion-APP\database\Book1.xlsx"
sales_file = r"D:\Doc\pyhton_projects\Gestion-APP\database\Sales_History.xlsx"

# Ensure directories exist
os.makedirs(os.path.dirname(products_file), exist_ok=True)
os.makedirs(os.path.dirname(sales_file), exist_ok=True)

# Load Products (Create if missing)
def load_products():
    try:
        return pd.read_excel(products_file)
    except FileNotFoundError:
        df = pd.DataFrame(columns=["Reference", "Designation", "QTX", "Prix Unitaire"])
        df.to_excel(products_file, index=False)
        return df

# Search for Products
def search_product(query):
    products_df = load_products()
    return products_df[
        products_df.apply(lambda row: query.lower() in str(row["Reference"]).lower() or 
                          query.lower() in str(row["Designation"]).lower(), axis=1)
    ]

# Sell Product (Update Stock)
def sell_product(ref, qty):
    products_df = load_products()

    if ref not in products_df["Reference"].values:
        return "Product not found."

    index = products_df[products_df["Reference"] == ref].index[0]
    
    if products_df.at[index, "QTX"] < qty:
        return "Not enough stock available."

    products_df.at[index, "QTX"] -= qty
    products_df.to_excel(products_file, index=False)

    # Log Sale
    log_sale(ref, qty, products_df.at[index, "Prix Unitaire"])

    return "Sale completed successfully."

# Log Sales
def log_sale(ref, qty, price):
    try:
        sales_df = pd.read_excel(sales_file)
    except FileNotFoundError:
        sales_df = pd.DataFrame(columns=["Reference", "Quantity", "Price", "Date"])

    new_sale = pd.DataFrame([[ref, qty, price, datetime.now().strftime("%Y-%m-%d %H:%M:%S")]], 
                            columns=["Reference", "Quantity", "Price", "Date"])
    
    sales_df = pd.concat([sales_df, new_sale], ignore_index=True)
    sales_df.to_excel(sales_file, index=False)

# Add New Product (Only Product Manager)
def add_product(ref, name, qty, price, username):
    products_df = load_products()

    role = authenticate(username, "admin_password_placeholder")  # Now correctly checks role
    if role != "Product Manager":
        return "Access Denied. Only Product Manager can add products."

    if ref in products_df["Reference"].values:
        return "Product already exists."

    new_product = pd.DataFrame([[ref, name, qty, price]], columns=["Reference", "Designation", "QTX", "Prix Unitaire"])
    products_df = pd.concat([products_df, new_product], ignore_index=True)
    products_df.to_excel(products_file, index=False)

    return "Product added successfully."
def view_sales_history(username):
    from auth import authenticate
    role = authenticate(username, "admin_password_placeholder")

    if role != "Admin":
        return "Access Denied. Only Admin can view sales history."

    try:
        sales_df = pd.read_excel(sales_file)
        return sales_df
    except FileNotFoundError:
        return pd.DataFrame(columns=["Reference", "Quantity", "Price", "Date"])
