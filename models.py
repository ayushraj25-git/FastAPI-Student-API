from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database_orm import Base

class Student(Base):
    __tablename__ = "students_orm"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    branch = Column(String, nullable=False)
    year = Column(Integer, nullable=False)
    email = Column(String, nullable=True)
    projects = relationship("Project", back_populates="student")


from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship


class Project(Base):
    __tablename__ = "student_projects"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)

    student_id = Column(
        Integer,
        ForeignKey("students_orm.id"),
        nullable=False
    )

    student = relationship("Student", back_populates="projects")
