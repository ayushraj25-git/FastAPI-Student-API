import pytest
from database import database_connection


def test_database_rollback():
    with pytest.raises(ValueError):
        with database_connection() as conn:
            cursor = conn.cursor()

            cursor.execute("""
                CREATE TABLE IF NOT EXISTS rollback_demo (
                    id INTEGER PRIMARY KEY,
                    name TEXT
                )
            """)

            cursor.execute(
                "INSERT INTO rollback_demo (name) VALUES (?)",
                ("Test Student",)
            )

            raise ValueError("Simulated error")

    with database_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM rollback_demo")
        result = cursor.fetchone()

    assert result is None
    with database_connection() as conn:
        conn.execute("DROP TABLE IF EXISTS rollback_demo")
        conn.commit()