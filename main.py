from fastapi import FastAPI, status, HTTPException,Depends
from pydantic import BaseModel, Field, StringConstraints
from typing import Annotated
from database import get_connection
from auth_utils import get_current_user


app=FastAPI()
@app.get("/")
def home():
    return{"message":"Hello Ayush"}

@app.get("/about")
def about():
    return{"message":"This is my first FastAPI project"}

@app.get("/student")
def get_students(username: str = Depends(get_current_user)):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students")
    students=cursor.fetchall()
    conn.close()
    return [dict(student) for student in students]
    
    

@app.get("/student/{student_id}")
def get_student(
    student_id: int,
    username: str = Depends(get_current_user)
):
    conn=get_connection()
    cursor=conn.cursor()
    cursor.execute("SELECT * FROM students where id = ?", (student_id,))
    student = cursor.fetchone()
    conn.close()
    if student is None:
     raise HTTPException(
        status_code=404,
        detail="Student not found"
    )
    return dict(student)

#query parameters
@app.get("/search")
def search_student(branch:str="CSE",year:int=3):
    return{"searched_branch":branch,"year":year}


NameType = Annotated[
    str,
    StringConstraints(min_length=2, strip_whitespace=True)
]

class Student(BaseModel):
    name: NameType
    branch: NameType
    year: int = Field(ge=1, le=4)


class StudentUpdate(BaseModel):
    name: NameType | None = None
    branch: NameType | None = None
    year: int | None = Field(default=None, ge=1, le=4)


@app.post("/student", status_code=status.HTTP_201_CREATED)
def add_student(
    student: Student,
    username: str = Depends(get_current_user)
):
    conn=get_connection()
    cursor=conn.cursor()


    cursor.execute(
    "INSERT INTO students (name, branch, year) VALUES (?, ?, ?)",
    (student.name, student.branch, student.year)
    )

    conn.commit()
    student_id=cursor.lastrowid
    conn.close()
    return{"message":"Student added successfully","student_id":student_id,"student":student}    

@app.put("/student/{student_id}")
def update_student(
    student_id: int,
    student: Student,
    username: str = Depends(get_current_user)
):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE students SET name = ?, branch = ?, year = ? WHERE id = ?",
        (student.name, student.branch, student.year, student_id)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404,detail="Student not found")
        

    conn.close()

    return {"message": "Student updated successfully"}


@app.patch("/student/{student_id}")
def patch_student(
    student_id: int,
    student: StudentUpdate,
    username: str = Depends(get_current_user)
):

    conn = get_connection()
    cursor = conn.cursor()

    updates = student.model_dump(exclude_unset=True)

    if not updates:
        conn.close()
        raise HTTPException(
            status_code=400,
            detail="No fields provided"
        )

    fields = ", ".join(f"{field} = ?" for field in updates)
    values = list(updates.values())
    values.append(student_id)

    cursor.execute(
        f"UPDATE students SET {fields} WHERE id = ?",
        values
    )

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(
            status_code=404,
            detail="Student not found"
        )

    conn.commit()
    conn.close()

    return {"message": "Student updated successfully"}

#DELETE

@app.delete("/student/{student_id}")
def delete_student(
    student_id: int,
    username: str = Depends(get_current_user)
):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM students WHERE id = ?",
        (student_id,)
    )

    conn.commit()

    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404,detail="Student not found")

    conn.close()

    return {"message": "Student deleted successfully"}


  
