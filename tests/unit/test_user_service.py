import uuid

from unittest.mock import MagicMock

from app.api.users.models import User
from app.api.users.repositories import UserRepository
from app.api.users.services import UserService


class TestUserService:
    """Tests for UserService with a mocked repository."""

    def test_get_user_profile(self):
        mock_repo = MagicMock(spec=UserRepository)
        user_id = uuid.uuid4()
        mock_repo.get_by_username.return_value = User(
            id=user_id, username="alice", name="Alice"
        )
        service = UserService(repository=mock_repo)

        result = service.get_user_profile("alice")

        assert result.id == user_id
        assert result.username == "alice"
        assert result.name == "Alice"
        mock_repo.get_by_username.assert_called_once_with("alice")

    def test_get_user_profile_none_name(self):
        mock_repo = MagicMock(spec=UserRepository)
        mock_repo.get_by_username.return_value = User(
            id=uuid.uuid4(), username="bob", name=None
        )
        service = UserService(repository=mock_repo)

        result = service.get_user_profile("bob")

        assert result.name is None
