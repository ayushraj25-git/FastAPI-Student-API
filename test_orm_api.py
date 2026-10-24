
from fastapi.testclient import TestClient
from orm_api import app

client = TestClient(app)


def test_home():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {
        "message": "SQLAlchemy ORM API is running"
    }


def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Test Student",
            "branch": "CSE",
            "year": 3,
            "email":"test@example.com"
        }
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Test Student"
    assert response.json()["branch"] == "CSE"


def test_get_students():
    response = client.get("/students")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_student_not_found():
    response = client.get("/students/999999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"


def test_update_student_not_found():
    response = client.put(
        "/students/999999",
        json={
            "name": "Updated Student",
            "branch": "CSE",
            "year": 3,
            "email":"updated@example.com"
        }
    )

    assert response.status_code == 404


def test_delete_student_not_found():
    response = client.delete("/students/999999")

    assert response.status_code == 404



def test_create_project():
    student_response = client.post(
        "/students",
        json={
            "name": "Project Test Student",
            "branch": "CSE",
            "year": 3,
            "email": "project.test@example.com"
        }
    )

    student_id = student_response.json()["id"]

    response = client.post(
        "/projects",
        json={
            "title": "Test Project",
            "student_id": student_id
        }
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Test Project"
    assert response.json()["student_id"] == student_id


def test_get_projects():
    response = client.get("/projects")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_create_project_student_not_found():
    response = client.post(
        "/projects",
        json={
            "title": "Invalid Project",
            "student_id": 999999
        }
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"



def test_get_student_projects():
    student_response = client.post(
        "/students",
        json={
            "name": "Relationship Test Student",
            "branch": "CSE",
            "year": 3,
            "email": "relationship.test@example.com"
        }
    )

    student_id = student_response.json()["id"]

    project_response = client.post(
        "/projects",
        json={
            "title": "Relationship Test Project",
            "student_id": student_id
        }
    )

    assert project_response.status_code == 200

    response = client.get(
        f"/students/{student_id}/projects"
    )

    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["title"] == "Relationship Test Project"
    assert response.json()[0]["student_id"] == student_id
