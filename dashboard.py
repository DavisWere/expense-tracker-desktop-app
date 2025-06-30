import tkinter as tk
from tkinter import ttk, messagebox
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from datetime import datetime
import os
import threading
import schedule
import time
import base64
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from email.mime.text import MIMEText
from gmail_auth import get_gmail_service
import socket
import json
import sys


from email_config import EMAIL_ADDRESS, TO_EMAIL

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

        threading.Thread(target=self.run_background_tasks, daemon=True).start()



    def build_ui(self):
        tk.Label(self, text=f"Welcome, {self.username}", font=("Arial", 16)).pack(pady=10)
        ttk.Button(self, text="Logout", command=self.logout).pack()
        ttk.Button(self, text="📄 Export PDF Report", command=self.generate_pdf_report).pack(pady=10)

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
    

    def generate_pdf_report(self, email=None, username=None, silent=True):
        now = datetime.now()
        filename = f"report_{now.strftime('%Y-%m-%d')}.pdf"
        filepath = os.path.join(os.getcwd(), filename)

        # Fallbacks if not passed
        email = email or self.username
        username = username or self.username

        transactions = get_transactions(email)
        income, expense = calculate_totals(email)
        balance = income - expense

        c = canvas.Canvas(filepath, pagesize=A4)
        width, height = A4

        # Header
        c.setFont("Helvetica-Bold", 16)
        c.drawString(1 * inch, height - 1 * inch, "Finance Tracker Monthly Report")
        c.setFont("Helvetica", 12)
        c.drawString(1 * inch, height - 1.3 * inch, f"User: {self.username}")
        c.drawString(1 * inch, height - 1.6 * inch, f"Period: {now.strftime('%B %Y')}")
        c.drawString(1 * inch, height - 2.0 * inch, f"Income: {income:.2f}")
        c.drawString(3 * inch, height - 2.0 * inch, f"Expenses: {expense:.2f}")
        c.drawString(5 * inch, height - 2.0 * inch, f"Balance: {balance:.2f}")

        # Table header
        y = height - 2.5 * inch
        c.setFont("Helvetica-Bold", 10)
        c.drawString(1 * inch, y, "Date")
        c.drawString(2.5 * inch, y, "Type")
        c.drawString(3.5 * inch, y, "Amount")
        c.drawString(4.5 * inch, y, "Category")
        c.drawString(6 * inch, y, "Note")

        # Transactions
        c.setFont("Helvetica", 9)
        y -= 0.2 * inch
        for tx in transactions:
            if y < 1 * inch:
                c.showPage()
                y = height - 1 * inch
            c.drawString(1 * inch, y, str(tx[1]))  # date
            c.drawString(2.5 * inch, y, str(tx[2]))  # type
            c.drawString(3.5 * inch, y, f"{tx[3]:.2f}")  # amount
            c.drawString(4.5 * inch, y, str(tx[4]))  # category
            c.drawString(6 * inch, y, str(tx[5]))  # note
            y -= 0.2 * inch

        c.save()
        if not silent:
            messagebox.showinfo("PDF Report", f"Report saved as:\n{filename}")
        return filepath

    def check_internet(self):
        try:
            socket.create_connection(("8.8.8.8", 53), timeout=3)
            return True
        except OSError:
            return False

    def send_email_with_pdf(self, filepath, email=None, retry_attempts=3, retry_delay=600):
        for attempt in range(retry_attempts):
            if not self.check_internet():
                print(f"[✖] No internet connection. Retrying in {retry_delay // 60} min...")
                time.sleep(retry_delay)
                continue

            try:
                service = get_gmail_service()

                message = MIMEMultipart()
                message["to"] = email
                message["from"] = EMAIL_ADDRESS
                message["subject"] = "📄 Finance Tracker Report"

                message.attach(MIMEText("Attached is your auto-generated finance report.", "plain"))

                with open(filepath, "rb") as f:
                    file_data = f.read()
                    filename = os.path.basename(filepath)
                    part = MIMEApplication(file_data, _subtype="pdf")
                    part.add_header("Content-Disposition", "attachment", filename=filename)
                    message.attach(part)

                raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()

                service.users().messages().send(userId="me", body={"raw": raw_message}).execute()

                print(f"[✔] Email sent via Gmail API: {filename}")
                return  # Exit if success

            except Exception as e:
                import traceback
                print(f"[✖] Gmail API Email error: {e}")
                traceback.print_exc()
                print(f"Retrying in {retry_delay // 60} min...")

            time.sleep(retry_delay)

    def run_background_tasks(self):
        def load_current_user():
            try:
                with open("current_user.json", "r") as f:
                    return json.load(f)  # returns dict with email and username
            except FileNotFoundError:
                print("❌ No user session found.")
                return None
            
        def job():
            user_data = load_current_user()
            if not user_data:
                return  # No user available

            email = user_data["email"]
            username = user_data.get("username", "User")

            # today = datetime.today().date()
            today = datetime(2025, 7, 1).date() 
            if today.day == 1:
                filepath = self.generate_pdf_report(email, username)
                self.send_email_with_pdf(filepath,email)
            else:
                print("⏭️ Not the 1st of the month, skipping email.")

        # Check daily at 08:00 AM
        schedule.every().day.at("08:00").do(job)
        # schedule.every(2).minutes.do(job)

        while True:
            schedule.run_pending()
            time.sleep(30)
