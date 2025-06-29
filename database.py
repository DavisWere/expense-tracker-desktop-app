import sqlite3

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT,
            type TEXT,
            amount REAL,
            category TEXT,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(date, tx_type, amount, category, note):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (date, type, amount, category, note)
        VALUES (?, ?, ?, ?, ?)
    ''', (date, tx_type, amount, category, note))
    conn.commit()
    conn.close()

def get_transactions():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT * FROM transactions ORDER BY date DESC')
    rows = c.fetchall()
    conn.close()
    return rows

def calculate_totals():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income'")
    income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense'")
    expense = c.fetchone()[0] or 0
    conn.close()
    return income, expense
