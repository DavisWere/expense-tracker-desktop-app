import tkinter as tk
from tkinter import ttk, messagebox
from auth import init_user_table, register_user, authenticate_user
from dashboard import DashboardPage

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
        self.username = ttk.Entry(self)
        self.username.pack(padx=100, fill="x")
        self.password = ttk.Entry(self, show="*")
        self.password.pack(padx=100, fill="x")
        ttk.Button(self, text="Login", command=self.login).pack(pady=10)
        ttk.Button(self, text="Register", command=lambda: controller.show_frame("RegisterPage")).pack()

    def login(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        user_id = authenticate_user(u, p)
        if user_id:
            self.controller.launch_dashboard(u, user_id)
        else:
            messagebox.showerror("Error", "Invalid credentials.")


class RegisterPage(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        ttk.Label(self, text="Register", font=("Arial", 16)).pack(pady=20)
        self.username = ttk.Entry(self)
        self.username.pack(padx=100, fill="x")
        self.password = ttk.Entry(self, show="*")
        self.password.pack(padx=100, fill="x")
        self.confirm = ttk.Entry(self, show="*")
        self.confirm.pack(padx=100, fill="x")
        ttk.Button(self, text="Create Account", command=self.register).pack(pady=10)
        ttk.Button(self, text="Back to Login", command=lambda: controller.show_frame("LoginPage")).pack()

    def register(self):
        u = self.username.get().strip()
        p = self.password.get().strip()
        cp = self.confirm.get().strip()
        if not u or not p or not cp:
            messagebox.showerror("Error", "All fields required.")
        elif p != cp:
            messagebox.showerror("Error", "Passwords do not match.")
        elif register_user(u, p):
            messagebox.showinfo("Success", "Account created. You can now log in.")
            self.controller.show_frame("LoginPage")
        else:
            messagebox.showerror("Error", "Username already exists.")


if __name__ == "__main__":
    app = FinanceApp()
    app.mainloop()
