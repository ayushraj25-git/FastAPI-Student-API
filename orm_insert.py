
from database_orm import SessionLocal
from models import Student

db = SessionLocal()

try:
    student = Student(
        name="Rahul",
        branch="CSE",
        year=3
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    print("Student added successfully!")
    print("ID:", student.id)
    print("Name:", student.name)
    print("Branch:", student.branch)
    print("Year:", student.year)

finally:
    db.close()
