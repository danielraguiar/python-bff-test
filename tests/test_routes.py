import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch
from app.models.models import UserData, AdminData

BASE_URL = "https://api-onecloud.multicloud.tivit.com/fake"

@pytest.fixture
def mock_health_response():
    return {"status": "ok", "message": "API is healthy"}

@pytest.fixture
def mock_user_response():
    return {
        "message": "Hello, user!",
        "data": {
            "name": "John Doe",
            "email": "john@example.com",
            "purchases": [
                {"id": 1, "item": "Laptop", "price": 2500.0},
                {"id": 2, "item": "Smartphone", "price": 1200.0},
            ],
        },
    }

@pytest.fixture
def mock_admin_response():
    return {
        "message": "Hello, admin!",
        "data": {
            "name": "Admin Master",
            "email": "admin@example.com",
            "reports": [
                {"id": 1, "title": "Monthly Sales", "status": "Completed"},
                {"id": 2, "title": "User Activity", "status": "Pending"},
            ],
        },
    }

@pytest.fixture
def mock_token_response():
    return {"access_token": "mocked_token", "token_type": "bearer"}


def test_health_check(client: TestClient, mock_health_response):
    with patch("httpx.get") as mock_get:
        mock_get.return_value.json.return_value = mock_health_response
        mock_get.return_value.status_code = 200
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == mock_health_response


def test_user_route(client: TestClient, test_db, mock_token_response, mock_user_response):
    with patch("httpx.get") as mock_get:
        mock_get.return_value.json.side_effect = [mock_token_response, mock_user_response]
        mock_get.return_value.status_code = 200

        response = client.get("/user")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello, user!"

        db = next(test_db())
        users = db.query(UserData).all()
        assert len(users) == 2
        assert users[0].name == "John Doe"
        assert users[0].email == "john@example.com"
        assert users[0].item == "Laptop"


def test_admin_route(client: TestClient, test_db, mock_token_response, mock_admin_response):
    with patch("httpx.get") as mock_get:
        mock_get.return_value.json.side_effect = [mock_token_response, mock_admin_response]
        mock_get.return_value.status_code = 200

        response = client.get("/admin")
        assert response.status_code == 200
        assert response.json()["message"] == "Hello, admin!"

        db = next(test_db())
        admins = db.query(AdminData).all()
        assert len(admins) == 2
        assert admins[0].name == "Admin Master"
        assert admins[0].email == "admin@example.com"
        assert admins[0].title == "Monthly Sales"
