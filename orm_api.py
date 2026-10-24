
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database_orm import engine, Base, get_db
from models import Student

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SQLAlchemy ORM API is running"}

@app.post("/students")
def create_student(
    name: str,
    branch: str,
    year: int,
    db: Session = Depends(get_db)
):
    student = Student(name=name, branch=branch, year=year)
    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "year": student.year
    }

@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return [
        {
            "id": student.id,
            "name": student.name,
            "branch": student.branch,
            "year": student.year
        }
        for student in students
    ]



@app.get("/students/{student_id}")
def get_student(student_id: int, db: Session = Depends(get_db)):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return {
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "year": student.year
    }



@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    name: str,
    branch: str,
    year: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    student.name = name
    student.branch = branch
    student.year = year

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "year": student.year
    }




@app.delete("/students/{student_id}")
def delete_student(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        from fastapi import HTTPException
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    db.delete(student)
    db.commit()

    return {"message": "Student deleted successfully"}
