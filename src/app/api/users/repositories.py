from sqlalchemy.orm import Session

from app.api.users import models
from app.helpers.exceptions import UnauthorizedException
from app.helpers.schemas import ApiError


class UserRepository:
    """Data access layer for user operations."""

    def __init__(self, database: Session) -> None:
        self.database = database

    def create(
        self,
        username: str,
        name: str = "",
    ) -> models.User:
        """
        Finds a user based on the provided JWT token. If the user does not exist, creates a new user.

        Args:
            username (str):
            name (str):
        Returns:
            model.User

        Raises:
            UnauthorizedException: If the token is invalid or cannot be decoded.
        """
        new_user = models.User(
            username=username,
            name=name,
        )

        self.database.add(new_user)
        self.database.commit()

        return new_user

    def get_by_username(self, username: str) -> models.User:
        """
        Finds a user based on the provided JWT token. If the user does not exist, creates a new user.

        Args:
            username (str):

        Returns:
            str: The user ID extracted from the JWT token.

        Raises:
            UnauthorizedException: If the token is invalid or cannot be decoded.
        """

        if not self._user_exists(username):
            user = self.create(username)
        else:
            user = self.database.query(models.User).filter_by(username=username).first()

        if user is None:
            error_response = ApiError(
                type="about:blank",
                title="Unauthorized",
                detail="Username can neither be stored nor retrieved.",
                instance=str(username),
            )
            raise UnauthorizedException(error_response.model_dump())

        return user

    def _user_exists(self, username: str) -> bool:
        """
        Checks if a user with the given username exists in the database.

        Args:
            username (str): The username to check for.

        Returns:
            bool: True if the user exists, False otherwise.
        """
        return (
            self.database.query(models.User).filter_by(username=username).first()
            is not None
        )
