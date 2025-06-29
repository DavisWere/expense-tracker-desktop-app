import tkinter as tk
from tkinter import ttk, messagebox
from auth import init_user_table, register_user, authenticate_user
import dashboard

init_user_table()

def open_dashboard(username):
    root.destroy()
    dashboard.launch_dashboard(username)

def login():
    username = username_entry.get()
    password = password_entry.get()
    if authenticate_user(username, password):
        open_dashboard(username)
    else:
        messagebox.showerror("Login Failed", "Invalid username or password.")

def register():
    username = username_entry.get().strip()
    password = password_entry.get().strip()
    confirm_password = confirm_password_entry.get().strip()

    if not username or not password or not confirm_password:
        messagebox.showerror("Error", "All fields are required.")
        return

    if password != confirm_password:
        messagebox.showerror("Error", "Passwords do not match.")
        return

    if register_user(username, password):
        messagebox.showinfo("Success", "Account created! You can now log in.")
        # Optionally: switch to login view or clear fields
        username_entry.delete(0, tk.END)
        password_entry.delete(0, tk.END)
        confirm_password_entry.delete(0, tk.END)
    else:
        messagebox.showerror("Error", "Username already exists.")


root = tk.Tk()
root.title("Login - Finance Tracker")
root.geometry("500x350")  # Make it wider & taller
root.resizable(True, True)  # Allow both directions


ttk.Label(root, text="Username:").pack(pady=(20, 5))
username_entry = ttk.Entry(root)
username_entry.pack()

ttk.Label(root, text="Password:").pack(pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.pack()

ttk.Button(root, text="Login", command=login).pack(pady=10)
ttk.Button(root, text="Register", command=register).pack()
ttk.Label(root, text="Username:").pack(pady=(20, 5))
username_entry = ttk.Entry(root)
username_entry.pack()

ttk.Label(root, text="Password:").pack(pady=5)
password_entry = ttk.Entry(root, show="*")
password_entry.pack()

ttk.Label(root, text="Confirm Password:").pack(pady=5)
confirm_password_entry = ttk.Entry(root, show="*")
confirm_password_entry.pack()


root.mainloop()

# 
# 