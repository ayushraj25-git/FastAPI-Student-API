# FastAPI Student Management API

A RESTful Student Management API built with **Python, FastAPI, and SQLite**, featuring JWT authentication, secure password hashing, SQLAlchemy ORM, student-project relationships, input validation, and automated testing.

## Features

- Student CRUD operations (Create, Read, Update, Delete)
- SQLite database integration
- SQLAlchemy ORM models and database sessions
- One-to-many relationship between students and projects
- Project creation and retrieval endpoints
- Retrieve all projects belonging to a student
- Foreign key constraints and referential integrity
- JWT-based authentication
- Password hashing using Argon2
- Protected API endpoints using bearer tokens
- Input validation using Pydantic
- Email validation using Pydantic EmailStr
- HTTP error handling (400, 401, 404, 422)
- Automated testing using Pytest
- Environment variables for secret-key configuration
- Dependency management using `requirements.txt`

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** SQLite
- **ORM:** SQLAlchemy
- **Authentication:** JWT (JSON Web Tokens)
- **Password Hashing:** Argon2
- **Validation:** Pydantic
- **Testing:** Pytest
- **Version Control:** Git and GitHub

## Project Structure

```text
FastAPI-Student-API/
├── main.py
├── auth_main.py
├── auth_utils.py
├── database.py
├── database_orm.py
├── models.py
├── schemas.py
├── orm_api.py
├── create_db.py
├── create_tables.py
├── create_users_table.py
├── insert_student.py
├── read_students.py
├── update_students.py
├── delete_student.py
├── orm_insert.py
├── orm_read.py
├── orm_update.py
├── orm_delete.py
├── test_main.py
├── test_auth.py
├── test_orm_api.py
├── requirements.txt
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/ayushraj25-git/FastAPI-Student-API.git
cd FastAPI-Student-API
```

### 2. Create and activate a virtual environment

Windows PowerShell:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

## Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=replace_with_a_secure_random_secret
```

Generate a secure secret key:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated value into `.env`. Never commit your actual secret key to GitHub.

## Running the Applications

Activate the virtual environment in each terminal.

### Terminal 1 — Authentication API

```bash
python -m uvicorn auth_main:app --reload --port 8000
```

### Terminal 2 — Student Management API

```bash
python -m uvicorn main:app --reload --port 8001
```

### Terminal 3 — SQLAlchemy ORM API

```bash
python -m uvicorn orm_api:app --reload --port 8002
```

The ORM API provides student CRUD operations and project management using SQLAlchemy ORM. It uses the `students_orm` and `student_projects` tables in the SQLite database.

## API Documentation

Open the interactive Swagger documentation after starting the corresponding server:

- **Authentication API:** http://127.0.0.1:8000/docs
- **Student Management API:** http://127.0.0.1:8001/docs
- **SQLAlchemy ORM API:** http://127.0.0.1:8002/docs

## SQLAlchemy ORM Endpoints

### Student endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | API health check |
| POST | `/students` | Create a student |
| GET | `/students` | Retrieve all students |
| GET | `/students/{student_id}` | Retrieve a student by ID |
| PUT | `/students/{student_id}` | Update a student |
| DELETE | `/students/{student_id}` | Delete a student |

### Project endpoints

| Method | Endpoint | Description |
|---|---|---|
| POST | `/projects` | Create a project for a student |
| GET | `/projects` | Retrieve all projects |
| GET | `/students/{student_id}/projects` | Retrieve projects belonging to a student |

Project creation checks whether the specified student exists. An invalid student ID returns HTTP 404.

## Student-Project Relationship

The project uses a one-to-many relationship:

- One student can have multiple projects.
- Each project belongs to one student.
- SQLAlchemy `relationship()` connects the `Student` and `Project` models.
- `ForeignKey` links `student_projects.student_id` to `students_orm.id`.
- SQLite foreign key enforcement helps prevent projects from referencing nonexistent students.

## Authentication Flow

1. Register a user using `POST /signup`.
2. Log in using `POST /login`.
3. Copy the returned access token.
4. Click **Authorize** in Swagger and enter the bearer token.
5. Access the protected student endpoints.

The JWT access token expires after 30 minutes.

## Testing

Run all automated tests:

```bash
python -m pytest -v
```

**Latest verified result: 45 tests passed.**

The test suites cover authentication, student CRUD operations, input validation, HTTP error handling, SQLAlchemy ORM operations, project creation, student-project relationships, and invalid student references.

## Learning Outcomes

This project demonstrates practical experience with:

- REST API development using FastAPI
- SQLite database operations and SQLAlchemy ORM
- CRUD operations and database sessions
- One-to-many database relationships
- Foreign key constraints and referential integrity
- JWT authentication and password security
- Request validation and HTTP error handling
- Environment variables and dependency management
- Automated testing with Pytest
- Version control and GitHub workflows

## Author

**Ayush Raj**

GitHub: https://github.com/ayushraj25-git

Repository: https://github.com/ayushraj25-git/FastAPI-Student-API


