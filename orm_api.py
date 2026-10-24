
from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from database_orm import engine, Base, get_db
from models import Student
from models import Project
from schemas import StudentCreate,ProjectCreate

Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "SQLAlchemy ORM API is running"}


@app.post("/students")
def create_student(
    data: StudentCreate,
    db: Session = Depends(get_db)
):
    student = Student(
        name=data.name,
        branch=data.branch,
        year=data.year,
        email=data.email
    )

    db.add(student)
    db.commit()
    db.refresh(student)

    return {
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "year": student.year,
        "email": student.email
    }


@app.get("/students")
def get_students(db: Session = Depends(get_db)):
    students = db.query(Student).all()

    return [
        {
            "id": student.id,
            "name": student.name,
            "branch": student.branch,
            "year": student.year,
            "email":student.email
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
        "year": student.year,
        "email":student.email
    }




@app.put("/students/{student_id}")
def update_student(
    student_id: int,
    data: StudentCreate,
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

    student.name = data.name
    student.branch = data.branch
    student.year = data.year
    student.email = data.email

    db.commit()
    db.refresh(student)

    return {
        "message": "Student updated successfully",
        "id": student.id,
        "name": student.name,
        "branch": student.branch,
        "year": student.year,
        "email": student.email
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




from fastapi import HTTPException


@app.post("/projects")
def create_project(
    data: ProjectCreate,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == data.student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    project = Project(
        title=data.title,
        student_id=data.student_id
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return {
        "id": project.id,
        "title": project.title,
        "student_id": project.student_id
    }



@app.get("/projects")
def get_projects(db: Session = Depends(get_db)):
    projects = db.query(Project).all()

    return [
        {
            "id": project.id,
            "title": project.title,
            "student_id": project.student_id
        }
        for project in projects
    ]



@app.get("/students/{student_id}/projects")
def get_student_projects(
    student_id: int,
    db: Session = Depends(get_db)
):
    student = db.query(Student).filter(
        Student.id == student_id
    ).first()

    if student is None:
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    return [
        {
            "id": project.id,
            "title": project.title,
            "student_id": project.student_id
        }
        for project in student.projects
    ]

