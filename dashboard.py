def launch_dashboard(username):
    import tkinter as tk
    import sqlite3
    from tkinter import ttk, messagebox
    from datetime import datetime
    from database import init_db, add_transaction, get_transactions, calculate_totals

    init_db()
    root = tk.Tk()
    root.title(f"💸 Finance Tracker - {username}")
    root.geometry("800x600")
    root.configure(bg="white")

    style = ttk.Style(root)
    style.configure("Treeview", font=("Arial", 11))
    style.configure("Treeview.Heading", font=("Arial", 12, "bold"))

    # ---- Add Transaction Frame ----
    frame = ttk.LabelFrame(root, text="Add Transaction", padding=10)
    frame.pack(padx=10, pady=10, fill='x')

    tk.Label(frame, text="Date (YYYY-MM-DD):").grid(row=0, column=0, sticky="w")
    date_entry = tk.Entry(frame)
    date_entry.insert(0, datetime.today().strftime('%Y-%m-%d'))
    date_entry.grid(row=0, column=1)

    tk.Label(frame, text="Type:").grid(row=0, column=2, sticky="w")
    type_combo = ttk.Combobox(frame, values=["Income", "Expense"], state="readonly")
    type_combo.grid(row=0, column=3)

    tk.Label(frame, text="Amount:").grid(row=1, column=0, sticky="w")
    amount_entry = tk.Entry(frame)
    amount_entry.grid(row=1, column=1)

    tk.Label(frame, text="Category:").grid(row=1, column=2, sticky="w")
    category_entry = tk.Entry(frame)
    category_entry.grid(row=1, column=3)

    tk.Label(frame, text="Note:").grid(row=2, column=0, sticky="w")
    note_entry = tk.Entry(frame, width=60)
    note_entry.grid(row=2, column=1, columnspan=3, pady=5)

    def submit_transaction():
        try:
            add_transaction(
                date_entry.get(),
                type_combo.get(),
                float(amount_entry.get()),
                category_entry.get(),
                note_entry.get()
            )
            messagebox.showinfo("Success", "Transaction added!")
            refresh_data()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    ttk.Button(frame, text="Add", command=submit_transaction).grid(row=3, column=3, sticky="e")

    # ---- Filter Frame ----
    filter_frame = ttk.LabelFrame(root, text="Filters", padding=10)
    filter_frame.pack(fill='x', padx=10, pady=(0, 10))

    tk.Label(filter_frame, text="Start Date:").grid(row=0, column=0)
    start_date = tk.Entry(filter_frame)
    start_date.grid(row=0, column=1)

    tk.Label(filter_frame, text="End Date:").grid(row=0, column=2)
    end_date = tk.Entry(filter_frame)
    end_date.grid(row=0, column=3)

    tk.Label(filter_frame, text="Category:").grid(row=0, column=4)
    category_filter = tk.Entry(filter_frame)
    category_filter.grid(row=0, column=5)

    def apply_filter():
        query = "SELECT * FROM transactions WHERE 1=1"
        values = []

        if start_date.get():
            query += " AND date >= ?"
            values.append(start_date.get())
        if end_date.get():
            query += " AND date <= ?"
            values.append(end_date.get())
        if category_filter.get():
            query += " AND category LIKE ?"
            values.append(f"%{category_filter.get()}%")

        conn = sqlite3.connect('finance.db')
        c = conn.cursor()
        c.execute(query, values)
        rows = c.fetchall()
        conn.close()

        tree.delete(*tree.get_children())
        for tx in rows:
            tree.insert('', 'end', values=tx)

    ttk.Button(filter_frame, text="Apply", command=apply_filter).grid(row=0, column=6, padx=5)

    # ---- Transactions Table ----
    table_frame = ttk.LabelFrame(root, text="Transaction History", padding=10)
    table_frame.pack(padx=10, pady=10, fill='both', expand=True)

    columns = ("id", "date", "type", "amount", "category", "note")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings")
    for col in columns:
        tree.heading(col, text=col.capitalize())
        tree.column(col, anchor="center")
    tree.pack(fill='both', expand=True)

    # ---- Summary ----
    summary_label = tk.Label(root, text="", font=("Arial", 14), bg="white")
    summary_label.pack(pady=10)

    def refresh_data():
        for row in tree.get_children():
            tree.delete(row)
        for tx in get_transactions():
            tree.insert('', 'end', values=tx)

        income, expense = calculate_totals()
        balance = income - expense
        summary_label.config(
            text=f"💰 Income: {income:.2f} | 💸 Expense: {expense:.2f} | 🧮 Balance: {balance:.2f}"
        )

    refresh_data()
    root.mainloop()


