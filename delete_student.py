import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute(
    "DELETE FROM students WHERE name = ?",
    ("Rahul",)
)

conn.commit()
conn.close()

print("Student deleted successfully!")