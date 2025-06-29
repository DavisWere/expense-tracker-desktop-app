import sqlite3

def init_db():
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            date TEXT,
            type TEXT,
            amount REAL,
            category TEXT,
            note TEXT
        )
    ''')
    conn.commit()
    conn.close()

def add_transaction(user_id, date, tx_type, amount, category, note):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO transactions (user_id, date, type, amount, category, note)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (user_id, date, tx_type, amount, category, note))
    conn.commit()
    conn.close()

def get_transactions(user_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute('SELECT id, date, type, amount, category, note FROM transactions WHERE user_id = ? ORDER BY date DESC', (user_id,))
    rows = c.fetchall()
    conn.close()
    return rows

def calculate_totals(user_id):
    conn = sqlite3.connect('finance.db')
    c = conn.cursor()
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Income' AND user_id=?", (user_id,))
    income = c.fetchone()[0] or 0
    c.execute("SELECT SUM(amount) FROM transactions WHERE type='Expense' AND user_id=?", (user_id,))
    expense = c.fetchone()[0] or 0
    conn.close()
    return income, expense
