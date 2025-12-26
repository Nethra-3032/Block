import sqlite3


def get_db_connection():
    conn = sqlite3.connect("bank.db", check_same_thread=False)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # Users table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE,
            password TEXT,
            balance REAL DEFAULT 0
        )
        """
    )

    # Transactions table
    cur.execute(
        """
        CREATE TABLE IF NOT EXISTS transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            sender TEXT,
            receiver TEXT,
            amount REAL,
            frequency INTEGER,
            status TEXT
        )
        """
    )

    conn.commit()
    conn.close()





