import sqlite3

conn = sqlite3.connect("finance.db")
c = conn.cursor()


try:
    c.execute("ALTER TABLE transactions ADD COLUMN user_id INTEGER DEFAULT 1")
    print("user_id column added.")
except sqlite3.OperationalError as e:
    print("Migration skipped:", e)

conn.commit()
conn.close()
