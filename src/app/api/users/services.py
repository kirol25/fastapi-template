from sqlalchemy.orm import Session

from app.api.users import schemas
from app.api.users.repositories import (
    UserRepository,
)


class UserService:
    def __init__(self, database: Session, language_code: str) -> None:
        self.repository = UserRepository(database, language_code)

    def get_user_profile(self, username: str) -> schemas.UserResponse:
        """
        Fetch the user from the database.

        Args:
            username (str): The extracted username from the Access Token.
            language_code (str): Extracted language code from Header request.

        Returns:
            UserResponse: The user data with all information related to that user.
        """
        user = self.repository.get_by_username(username)

        return schemas.UserResponse(
            id=user.id,
            username=user.username,
            name=user.name,
        )
