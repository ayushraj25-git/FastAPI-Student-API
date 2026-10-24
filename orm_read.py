
from database_orm import SessionLocal
from models import Student

db = SessionLocal()

try:
    students = db.query(Student).all()

    for student in students:
        print("ID:", student.id)
        print("Name:", student.name)
        print("Branch:", student.branch)
        print("Year:", student.year)
        print("-" * 20)

finally:
    db.close()
