
from database_orm import SessionLocal
from models import Student

db = SessionLocal()

try:
    student = db.query(Student).filter(Student.id == 1).first()

    if student:
        student.name = "Ayush"
        student.branch = "CSE-DS"
        db.commit()
        db.refresh(student)

        print("Student updated successfully!")
        print("ID:", student.id)
        print("Name:", student.name)
        print("Branch:", student.branch)
    else:
        print("Student not found!")

finally:
    db.close()
