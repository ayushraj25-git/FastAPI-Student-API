from fastapi.testclient import TestClient
from auth_main import app

client = TestClient(app)


def test_protected_without_token():
    response = client.get("/protected")

    assert response.status_code == 401


def test_signup():
    import uuid

    username = f"test_user_{uuid.uuid4().hex[:8]}"

    response = client.post(
        "/signup",
        json={
            "username": username,
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 201 


def test_login():
    response = client.post(
        "/login",
        json={
            "username": "auto_test_user_789",
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"  


def test_login_wrong_password():
    import uuid

    username = f"wrong_pass_{uuid.uuid4().hex[:8]}"

    # Pehle user register karo
    signup_response = client.post(
        "/signup",
        json={
            "username": username,
            "password": "SecurePass123"
        }
    )

    assert signup_response.status_code == 201

    # Ab galat password se login try karo
    response = client.post(
        "/login",
        json={
            "username": username,
            "password": "WrongPassword123"
        }
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid username or password"      


def test_signup_duplicate_username():
    import uuid

    username = f"duplicate_{uuid.uuid4().hex[:8]}"

    user_data = {
        "username": username,
        "password": "SecurePass123"
    }

    # Pehli baar signup
    first_response = client.post(
        "/signup",
        json=user_data
    )
    assert first_response.status_code == 201

    # Wahi username dobara use karo
    second_response = client.post(
        "/signup",
        json=user_data
    )

    assert second_response.status_code == 409
    assert second_response.json()["detail"] == "Username already exists" 



def test_signup_short_username():
    response = client.post(
        "/signup",
        json={
            "username": "ab",
            "password": "SecurePass123"
        }
    )

    assert response.status_code == 422


def test_signup_short_password():
    response = client.post(
        "/signup",
        json={
            "username": "valid_user",
            "password": "123"
        }
    )

    assert response.status_code == 422       