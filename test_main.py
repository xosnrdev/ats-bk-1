from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_create_user():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "email": "john.doe@example.com",
        "height": 180.5,
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201


def test_duplicate_email():
    user_data = {
        "first_name": "Jane",
        "last_name": "Smith",
        "age": 28,
        "email": "john.doe@example.com",
        "height": 165.0,
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400


def test_duplicate_email_case_insensitive():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "email": "JOHN.DOE@example.com",
        "height": 180.5,
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 400


def test_invalid_email():
    user_data = {
        "first_name": "John",
        "last_name": "Doe",
        "age": 30,
        "email": "invalid-email",
        "height": 180.5,
    }
    response = client.post("/users/", json=user_data)
    assert response.status_code == 422
