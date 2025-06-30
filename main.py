import tkinter as tk
from tkinter import ttk, messagebox
from auth import init_user_table, register_user, authenticate_user
from dashboard import DashboardPage
import json

class FinanceApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Finance Tracker")
        self.geometry("1000x700")
        self.resizable(True, True)

        self.container = tk.Frame(self)
        self.container.pack(fill="both", expand=True)

        self.frames = {}
        init_user_table()

        for Page in (LoginPage, RegisterPage):
            name = Page.__name__
            frame = Page(parent=self.container, controller=self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("LoginPage")

    def show_frame(self, name):
        frame = self.frames[name]
        frame.tkraise()

    def launch_dashboard(self, username, user_id):
        page = DashboardPage(self.container, self, username, user_id)
        self.frames["DashboardPage"] = page
        page.grid(row=0, column=0, sticky="nsew")
        self.show_frame("DashboardPage")


class LoginPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Login", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self, text="Email").pack(padx=100, anchor="w")
        self.email = ttk.Entry(self)
        self.email.pack(padx=100, fill="x")

        ttk.Label(self, text="Password").pack(padx=100, anchor="w")
        self.password = ttk.Entry(self, show="*")
        self.password.pack(padx=100, fill="x")

        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).pack()

    def login(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        user_id = authenticate_user(email, password)

        if user_id:
            # 🔐 Save session to disk for background access
            user_data = {
                "email": email,
                "user_id": user_id
            }
            with open("current_user.json", "w") as f:
                json.dump(user_data, f)

            self.controller.launch_dashboard(email, user_id)
        else:
            messagebox.showerror("Error", "Invalid email or password.")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Register", font=("Arial", 16)).pack(pady=20)

        ttk.Label(self, text="Email").pack(padx=100, anchor="w")
        self.email = ttk.Entry(self)
        self.email.pack(padx=100, fill="x")

        ttk.Label(self, text="Password").pack(padx=100, anchor="w")
        self.password = ttk.Entry(self, show="*")
        self.password.pack(padx=100, fill="x")

        ttk.Label(self, text="Confirm Password").pack(padx=100, anchor="w")
        self.confirm = ttk.Entry(self, show="*")
        self.confirm.pack(padx=100, fill="x")

        ttk.Button(self, text="Create Account", command=self.register).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginPage")).pack()

    def register(self):
        email = self.email.get().strip()
        password = self.password.get().strip()
        confirm = self.confirm.get().strip()

        if not email or not password or not confirm:
            messagebox.showerror("Error", "All fields are required.")
        elif password != confirm:
            messagebox.showerror("Error", "Passwords do not match.")
        elif register_user(email, password):  # register_user should expect email now
            messagebox.showinfo("Success", "Account created. You can now log in.")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Email already exists.")



if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
