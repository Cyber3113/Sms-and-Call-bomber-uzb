import sqlite3

conn = sqlite3.connect("users.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    username TEXT,
    phone TEXT
)
""")
conn.commit()

def add_user(user_id, first_name, last_name, username):
    cursor.execute("SELECT id FROM users WHERE id = ?", (user_id,))
    if cursor.fetchone() is None:
        cursor.execute("""
            INSERT INTO users (id, first_name, last_name, username, phone)
            VALUES (?, ?, ?, ?, NULL)
        """, (user_id, first_name, last_name, username))
        conn.commit()

def get_user(user_id):
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

def update_phone(user_id, phone):
    cursor.execute("UPDATE users SET phone = ? WHERE id = ?", (phone, user_id))
    conn.commit()
