# FastAPI Student Management API

A RESTful Student Management API built with **FastAPI, Python, and SQLite**, featuring JWT authentication, secure password hashing, input validation, and automated testing.

## Features

- Student CRUD operations (Create, Read, Update, Delete)
- SQLite database integration
- JWT-based authentication
- Password hashing using Argon2
- Protected API endpoints using bearer tokens
- Input validation using Pydantic
- Proper HTTP error handling
- Automated tests using Pytest
- Environment variables for secret-key configuration

## Tech Stack

- **Language:** Python
- **Framework:** FastAPI
- **Database:** SQLite
- **Authentication:** JWT
- **Password Hashing:** Argon2
- **Testing:** Pytest
- **Validation:** Pydantic

## Project Structure

```text
FastAPI_Project/
├── main.py
├── auth_main.py
├── auth_utils.py
├── database.py
├── create_db.py
├── create_users_table.py
├── insert_student.py
├── read_students.py
├── update_students.py
├── delete_student.py
├── test_main.py
├── test_auth.py
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
python -m pip install fastapi "uvicorn[standard]" PyJWT pwdlib[argon2] python-dotenv pytest httpx
```

## Environment Configuration

Create a `.env` file in the project root:

```env
SECRET_KEY=replace_with_a_secure_random_secret
```

Generate a secure secret key using:

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

Copy the generated value into `.env`. Never commit your actual secret key to GitHub.

## Running the Application

Open two terminals from the project directory and activate the virtual environment in each.

**Terminal 1 — Authentication API**

```bash
python -m uvicorn auth_main:app --reload --port 8000
```

**Terminal 2 — Student API**

```bash
python -m uvicorn main:app --reload --port 8001
```

## API Documentation

After starting the servers, open the interactive Swagger documentation:

- Authentication API: http://127.0.0.1:8000/docs
- Student API: http://127.0.0.1:8001/docs

## Authentication Flow

1. Register a user using `POST /signup`.
2. Log in using `POST /login`.
3. Copy the returned access token.
4. Use the **Authorize** button in the Student API Swagger documentation and enter the bearer token.
5. Access the protected student endpoints.

The JWT access token expires after 30 minutes.

## Testing

Run the test suite:

```bash
python -m pytest -v
```

**Latest test result:** 33 passed.

## Learning Outcomes

This project demonstrates practical experience with REST APIs, database operations, authentication, password security, request validation, environment variables, Git, and automated testing.

## Author

**Ayush Raj**

GitHub: [@ayushraj25-git](https://github.com/ayushraj25-git)
