
from pydantic import BaseModel, EmailStr


class StudentCreate(BaseModel):
    name: str
    branch: str
    year: int
    email: EmailStr | None = None
