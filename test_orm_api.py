
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
        params={
            "name": "Test Student",
            "branch": "CSE",
            "year": 3
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
        params={
            "name": "Updated Student",
            "branch": "CSE",
            "year": 3
        }
    )

    assert response.status_code == 404


def test_delete_student_not_found():
    response = client.delete("/students/999999")

    assert response.status_code == 404
