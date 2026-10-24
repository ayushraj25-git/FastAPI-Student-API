
from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    branch: str
    year: int
    email: EmailStr | None = None


class ProjectCreate(BaseModel):
    title: str
    student_id: int
