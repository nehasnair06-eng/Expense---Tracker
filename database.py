import sqlite3

DB_NAME = "expenses.db"


def connect_db():
    return sqlite3.connect(DB_NAME)


def create_table():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            category TEXT NOT NULL,
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT
        )
    """)

    conn.commit()
    conn.close()


def add_expense(title, category, amount, date, description):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO expenses
        (title, category, amount, date, description)
        VALUES (?, ?, ?, ?, ?)
    """, (title, category, amount, date, description))

    conn.commit()
    conn.close()


def get_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, category, amount, date, description
        FROM expenses
        ORDER BY id DESC
    """)

    data = cursor.fetchall()

    conn.close()

    return data


def delete_expense(expense_id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM expenses WHERE id = ?",
        (expense_id,)
    )

    conn.commit()
    conn.close()