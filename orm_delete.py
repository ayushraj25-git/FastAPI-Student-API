
from database_orm import SessionLocal
from models import Student

db = SessionLocal()

try:
    student = db.query(Student).filter(Student.id == 1).first()

    if student:
        db.delete(student)
        db.commit()
        print("Student deleted successfully!")
    else:
        print("Student not found!")

finally:
    db.close()
