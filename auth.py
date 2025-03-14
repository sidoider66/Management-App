import pandas as pd
import bcrypt
import os

# Define file path
users_file = r"D:\Doc\pyhton_projects\Gestion-APP\database\users.xlsx"

# Ensure directory exists
os.makedirs(os.path.dirname(users_file), exist_ok=True)

# Load Users Data (Create if missing)
def load_users():
    try:
        users_df = pd.read_excel(users_file)
    except FileNotFoundError:
        users_df = pd.DataFrame(columns=["Username", "Password", "Role"])
        users_df.to_excel(users_file, index=False)
        return users_df

    # Ensure an admin exists
    if "admin" not in users_df["Username"].values:
        hashed_password = bcrypt.hashpw("admin123".encode(), bcrypt.gensalt()).decode()
        admin_user = pd.DataFrame([["admin", hashed_password, "Admin"]], columns=["Username", "Password", "Role"])
        users_df = pd.concat([users_df, admin_user], ignore_index=True)
        users_df.to_excel(users_file, index=False)

    return users_df

# Authenticate User
def authenticate(username, password):
    users_df = load_users()
    user_row = users_df[users_df["Username"] == username]

    if not user_row.empty:
        stored_hashed_password = user_row.iloc[0]["Password"]
        role = user_row.iloc[0]["Role"]
        
        # Check hashed password
        if bcrypt.checkpw(password.encode(), stored_hashed_password.encode()):
            return role
    return None

# Register a New User (Only Admins)
def register_user(username, password, role, admin_username):
    users_df = load_users()

    if username in users_df["Username"].values:
        return "User already exists!"

    if authenticate(admin_username, "admin_password_placeholder") != "Admin":
        return "Only admins can add users!"

    # Hash password before storing
    hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()

    new_user = pd.DataFrame([[username, hashed_password, role]], columns=["Username", "Password", "Role"])
    users_df = pd.concat([users_df, new_user], ignore_index=True)
    users_df.to_excel(users_file, index=False)

    return "User registered successfully!"

