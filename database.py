import sqlite3


def get_connection():
    conn = sqlite3.connect(
        "students.db",
        timeout=10
    )
    conn.row_factory = sqlite3.Row
    return conn
