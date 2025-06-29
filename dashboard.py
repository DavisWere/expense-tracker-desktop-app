import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from database import init_db, add_transaction, get_transactions, calculate_totals

class DashboardPage(tk.Frame):
    def __init__(self, parent, controller, username, user_id):
        super().__init__(parent)
        self.controller = controller
        self.username = username
        self.user_id = user_id

        init_db()
        self.build_ui()
        self.refresh_data()

    def build_ui(self):
        tk.Label(self, text=f"Welcome, {self.username}", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self, text="Logout", command=self.logout).pack()

        frame = ttk.LabelFrame(self, text="Add Transaction")
        frame.pack(padx=10, pady=10, fill="x")

        self.date_entry = tk.Entry(frame)
        self.date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
        self.type_combo = ttk.Combobox(frame, values=["Income", "Expense"], state="readonly")
        self.amount_entry = tk.Entry(frame)
        self.category_entry = tk.Entry(frame)
        self.note_entry = tk.Entry(frame, width=50)

        labels = ["Date (YYYY-MM-DD):", "Type:", "Amount:", "Category:", "Note:"]
        widgets = [self.date_entry, self.type_combo, self.amount_entry, self.category_entry, self.note_entry]
        for i, (label, widget) in enumerate(zip(labels, widgets)):
            tk.Label(frame, text=label).grid(row=i, column=0, sticky="w")
            widget.grid(row=i, column=1, padx=5, pady=3)

        ttk.Button(frame, text="Add", command=self.submit_transaction).grid(row=len(labels), column=1, sticky="e")

        self.tree = ttk.Treeview(self, columns=("id", "date", "type", "amount", "category", "note"), show="headings")
        for col in self.tree["columns"]:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, anchor="center")
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        self.summary_label = tk.Label(self, text="", font=("Arial", 14))
        self.summary_label.pack(pady=10)

    def submit_transaction(self):
        try:
            add_transaction(
                self.user_id,
                self.date_entry.get(),
                self.type_combo.get(),
                float(self.amount_entry.get()),
                self.category_entry.get(),
                self.note_entry.get()
            )
            messagebox.showinfo("Success", "Transaction added.")
            self.refresh_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def refresh_data(self):
        for row in self.tree.get_children():
            self.tree.delete(row)
        for tx in get_transactions(self.user_id):
            self.tree.insert("", "end", values=tx)
        income, expense = calculate_totals(self.user_id)
        balance = income - expense
        self.summary_label.config(text=f"💰 Income: {income:.2f} | 💸 Expense: {expense:.2f} | 🧮 Balance: {balance:.2f}")

    def logout(self):
        self.controller.show_frame("LoginPage")
