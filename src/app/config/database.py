from collections.abc import Iterator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.config import settings
from app.utils.enums import Environment

SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.DATABASE_USERNAME}:{settings.DATABASE_PASSWORD}@{settings.DATABASE_HOST}:{settings.DATABASE_PORT}/{settings.DATABASE_NAME}"
connect_args = {}

if Environment.dev != settings.ENVIRONMENT:
    connect_args = {"sslmode": "require"}

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args=connect_args)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    """Declarative base class for all SQLAlchemy models."""


def get_session() -> Iterator[Session]:
    """Create new database session.

    Yields:
        Database session.
    """

    session = SessionLocal()

    try:
        yield session
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
