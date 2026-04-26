import uuid
from unittest.mock import MagicMock

from fastapi.testclient import TestClient

from app.api.users.deps import get_service
from app.api.users.services import UserService
from app.main import app


class TestUsersEndpoint:
    """Integration tests for the /users/me endpoint."""

    def test_get_user_profile(self):
        mock_service = MagicMock(spec=UserService)
        user_id = uuid.uuid4()
        mock_service.get_user_profile.return_value = {
            "id": user_id,
            "username": "alice",
            "name": "Alice",
        }
        app.dependency_overrides[get_service] = lambda: mock_service

        with TestClient(app) as client:
            response = client.get("/users/me", params={"username": "alice"})

        assert response.status_code == 200
        data = response.json()
        assert data["username"] == "alice"
        assert data["name"] == "Alice"
        app.dependency_overrides.clear()

    def test_get_user_profile_missing_username(self):
        mock_service = MagicMock(spec=UserService)
        app.dependency_overrides[get_service] = lambda: mock_service

        with TestClient(app) as client:
            response = client.get("/users/me")

        assert response.status_code == 422
        app.dependency_overrides.clear()
