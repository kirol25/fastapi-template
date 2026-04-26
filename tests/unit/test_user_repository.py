from sqlalchemy.orm import Session

from app.api.users.models import User
from app.api.users.repositories import UserRepository


class TestUserRepository:
    """Tests for UserRepository against a real database session."""

    def test_create_user(self, db_session: Session):
        repo = UserRepository(database=db_session)

        user = repo.create(username="alice", name="Alice")

        assert user.username == "alice"
        assert user.name == "Alice"
        assert user.id is not None

    def test_create_user_default_name(self, db_session: Session):
        repo = UserRepository(database=db_session)

        user = repo.create(username="bob")

        assert user.username == "bob"
        assert user.name == ""

    def test_get_by_username_creates_when_missing(self, db_session: Session):
        repo = UserRepository(database=db_session)

        user = repo.get_by_username("newuser")

        assert user.username == "newuser"
        assert isinstance(user, User)

    def test_get_by_username_returns_existing(self, db_session: Session):
        repo = UserRepository(database=db_session)
        repo.create(username="existing", name="Existing User")

        user = repo.get_by_username("existing")

        assert user.username == "existing"
        assert user.name == "Existing User"

    def test_user_exists_false(self, db_session: Session):
        repo = UserRepository(database=db_session)

        assert repo._user_exists("nobody") is False

    def test_user_exists_true(self, db_session: Session):
        repo = UserRepository(database=db_session)
        repo.create(username="someone")

        assert repo._user_exists("someone") is True
