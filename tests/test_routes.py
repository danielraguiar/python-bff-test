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

        response_data = response.json()

        assert "message" in response_data, f"Resposta não contém 'message': {response_data}"
        assert response_data["message"] == "Hello, user!"

        assert "data" in response_data, f"Resposta não contém 'data': {response_data}"
        user_data = response_data["data"]
        assert user_data["name"] == "John Doe"
        assert user_data["email"] == "john@example.com"

        assert "purchases" in user_data, f"Dados do usuário não contém 'purchases': {user_data}"
        purchases = user_data["purchases"]
        assert len(purchases) == 2
        assert purchases[0] == {"id": 1, "item": "Laptop", "price": 2500}
        assert purchases[1] == {"id": 2, "item": "Smartphone", "price": 1200}

def test_admin_route(client: TestClient, test_db, mock_token_response, mock_admin_response):
    with patch("httpx.get") as mock_get:
        mock_get.return_value.json.side_effect = [mock_token_response, mock_admin_response]
        mock_get.return_value.status_code = 200

        response = client.get("/admin")
        assert response.status_code == 200

        response_data = response.json()

        assert "message" in response_data, f"Resposta não contém 'message': {response_data}"
        assert response_data["message"] == "Hello, admin!"

        assert "data" in response_data, f"Resposta não contém 'data': {response_data}"
        admin_data = response_data["data"]
        assert admin_data["name"] == "Admin Master"
        assert admin_data["email"] == "admin@example.com"

        assert "reports" in admin_data, f"Dados do administrador não contém 'reports': {admin_data}"
        reports = admin_data["reports"]
        assert len(reports) == 2
        assert reports[0] == {"id": 1, "title": "Monthly Sales", "status": "Completed"}
        assert reports[1] == {"id": 2, "title": "User Activity", "status": "Pending"}
