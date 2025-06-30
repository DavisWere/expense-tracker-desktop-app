import sqlite3

conn = sqlite3.connect("finance.db")
c = conn.cursor()

# Add user_id column (if not exists)
try:
    c.execute("ALTER TABLE transactions ADD COLUMN user_id INTEGER DEFAULT 1")
    print("user_id column added.")
except sqlite3.OperationalError as e:
    print("user_id migration skipped:", e)

#Add user_email column
try:
    c.execute("ALTER TABLE transactions ADD COLUMN user_email TEXT")
    print("user_email column added.")
except sqlite3.OperationalError as e:
    print("user_email migration skipped:", e)

conn.commit()
conn.close()
