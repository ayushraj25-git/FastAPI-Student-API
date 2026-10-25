import sqlite3
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATABASE_PATH = BASE_DIR / "students.db"


def get_connection():
    conn = sqlite3.connect(
        DATABASE_PATH,
        timeout=10
    )
    conn.row_factory = sqlite3.Row
    return conn

from contextlib import contextmanager


@contextmanager
def database_connection():
    conn = get_connection()
    try:
        yield conn
    finally:
        conn.close()