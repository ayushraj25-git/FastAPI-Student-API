
from fastapi.testclient import TestClient
from main import app
from auth_utils import SECRET_KEY, ALGORITHM
import jwt
from datetime import datetime, timedelta, timezone
import pytest

client = TestClient(app)

@pytest.fixture
def auth_headers():
    token = jwt.encode(
        {
            "sub": "ayush_test",
            "exp": datetime.now(timezone.utc) + timedelta(minutes=30)
        },
        SECRET_KEY,
        algorithm=ALGORITHM
    )
    return {"Authorization": f"Bearer {token}"}


@pytest.fixture
def sample_student():
    return {
        "name": "Rahul Test",
        "branch": "CSE",
        "year": 2
    }
def test_home():
    response=client.get("/")

    assert response.status_code==200
    assert response.json()=={"message":"Hello Ayush"}


def test_about():
    response = client.get("/about")

    assert response.status_code == 200
    assert response.json() == {
        "message": "This is my first FastAPI project"
    }    


def test_search_default():
    response = client.get("/search")

    assert response.status_code == 200
    assert response.json() == {
        "searched_branch": "CSE",
        "year": 3
    }


def test_search_custom_parameters():
    response = client.get("/search?branch=IT&year=2")

    assert response.status_code == 200
    assert response.json() == {
        "searched_branch": "IT",
        "year": 2
    }

def test_get_students(auth_headers):
    response = client.get(
        "/student",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert isinstance(response.json(), list)  



def test_add_student(sample_student, auth_headers):
    response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    assert response.status_code == 201
    assert response.json()["message"] == "Student added successfully"



def test_get_student(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.get(
        f"/student/{student_id}",
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["id"] == student_id
    assert response.json()["name"] == sample_student["name"]




def test_update_student(auth_headers):
    create_response = client.post(
        "/student",
        json={
            "name": "Rahul Test",
            "branch": "CSE",
            "year": 2
        },
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.put(
        f"/student/{student_id}",
        json={
            "name": "Aman Test",
            "branch": "IT",
            "year": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 200
    assert response.json()["message"] == "Student updated successfully"

    get_response = client.get(
        f"/student/{student_id}",
        headers=auth_headers
    )
    assert get_response.json()["name"] == "Aman Test"
    assert get_response.json()["branch"] == "IT"
    assert get_response.json()["year"] == 3
  




def test_patch_student(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={"year": 4},
        headers=auth_headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/student/{student_id}",
        headers=auth_headers
    )
    data = get_response.json()

    assert data["year"] == 4
    assert data["name"] == sample_student["name"]
    assert data["branch"] == sample_student["branch"]
   




def test_delete_student(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.delete(
        f"/student/{student_id}",
        headers=auth_headers
    )

    assert response.status_code == 200

    get_response = client.get(
        f"/student/{student_id}",
        headers=auth_headers
    )

    assert get_response.status_code == 404




def test_update_nonexistent_student(auth_headers):
    response = client.put(
        "/student/999999",
        json={
            "name": "Aman Test",
            "branch": "IT",
            "year": 3
        },
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"





def test_patch_nonexistent_student(auth_headers):
    response = client.patch(
        "/student/999999",
        json={"year": 3},
        headers=auth_headers
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student not found"




def test_patch_invalid_year(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={"year": 6},
        headers=auth_headers
    )

    assert response.status_code == 422


def test_patch_year_non_integer(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={"year": "abc"},
        headers=auth_headers
    )

    assert response.status_code == 422







def test_patch_empty_data(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={},
        headers=auth_headers
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "No fields provided"



@pytest.mark.parametrize("year", [0, 5, 10])
def test_add_student_invalid_year(sample_student, year, auth_headers):
    sample_student["year"] = year

    response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    assert response.status_code == 422




@pytest.mark.parametrize("name", ["A", "", " "])
def test_add_student_short_name(sample_student, name, auth_headers):
    sample_student["name"] = name

    response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    assert response.status_code == 422



def test_patch_short_name(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={"name": "A"},
        headers=auth_headers
    )

    assert response.status_code == 422


def test_patch_short_branch(sample_student, auth_headers):
    create_response = client.post(
        "/student",
        json=sample_student,
        headers=auth_headers
    )

    student_id = create_response.json()["student_id"]

    response = client.patch(
        f"/student/{student_id}",
        json={"branch": "A"},
        headers=auth_headers
    )

    assert response.status_code == 422





def test_sample_student(sample_student):
    assert sample_student["name"] == "Rahul Test"
    assert sample_student["year"] == 2



def test_add_student_without_token():
    response = client.post(
        "/student",
        json={
            "name": "Test Student",
            "branch": "CSE",
            "year": 2
        }
    )
    assert response.status_code == 401


def test_update_student_without_token():
    response = client.put(
        "/student/1",
        json={
            "name": "Test Student",
            "branch": "CSE",
            "year": 2
        }
    )
    assert response.status_code == 401


def test_patch_student_without_token():
    response = client.patch(
        "/student/1",
        json={"name": "Test Student"}
    )
    assert response.status_code == 401


def test_delete_student_without_token():
    response = client.delete("/student/1")
    assert response.status_code == 401    