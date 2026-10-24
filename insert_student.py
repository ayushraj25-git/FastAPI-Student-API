import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute(
    "INSERT INTO students (name, branch, year) VALUES (?, ?, ?)",
    ("Rahul", "CSE", 3)
)

conn.commit()
conn.close()

print("Student added successfully!")
