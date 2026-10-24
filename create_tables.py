
from database_orm import engine, Base
from models import Student

Base.metadata.create_all(bind=engine)

print("SQLAlchemy tables created successfully!")
