import sqlite3

conn = sqlite3.connect("students.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM students WHERE name = ?",("Rahul",))

students = cursor.fetchall()

for student in students:
    print(student)

conn.close()