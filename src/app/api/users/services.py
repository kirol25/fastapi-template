from app.api.users import schemas
from app.api.users.repositories import (
    UserRepository,
)


class UserService:
    """Business logic layer for user operations."""

    def __init__(self, repository: UserRepository) -> None:
        self.repository = repository

    def get_user_profile(self, username: str) -> schemas.UserResponse:
        """
        Fetch the user from the database.

        Args:
            username (str): The extracted username from the Access Token.

        Returns:
            UserResponse: The user data with all information related to that user.
        """
        user = self.repository.get_by_username(username)

        return schemas.UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
        )
