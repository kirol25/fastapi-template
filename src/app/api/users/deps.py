from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.api.users.repositories import UserRepository
from app.api.users.services import UserService
from app.config.database import get_session

SessionDep = Annotated[Session, Depends(get_session)]


def get_repository(
    db: SessionDep,
) -> UserRepository:
    """Return a UserRepository with an injected database session."""
    return UserRepository(database=db)


def get_service(
    repo: Annotated[UserRepository, Depends(get_repository)],
) -> UserService:
    """Instantiate a UserService backed by the injected repository."""
    return UserService(repository=repo)


RepositoryDep = Annotated[UserRepository, Depends(get_repository)]
ServiceDep = Annotated[UserService, Depends(get_service)]
