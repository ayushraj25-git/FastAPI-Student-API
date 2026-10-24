import sqlite3
conn=sqlite3.connect("students.db")
cursor=conn.cursor()
cursor.execute("UPDATE students SET branch = ? WHERE name = ?",("IT","Rahul"))
conn.commit()
conn.close()
print("Student updated successfully! ")