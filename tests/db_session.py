import json
from collections.abc import Iterator
from pathlib import Path

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker

from app.config.database import Base

DATABASE_URL = "sqlite:///:memory:"

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# drop all tables on start-up and re-create them
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)


def override_get_db() -> Iterator[Session]:
    session = None
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        if session is not None:
            session.close()


def load_initial_data(db: Session) -> None:
    """
    Load default data into the test database.

    This function initializes the test database with default data by calling
    helper functions.

    Args:
        db (Session): The database session object.
    """
    pass


def _read_data_from_json(json_data_file: Path) -> dict:
    """
    Helper function to read data from a JSON file.

    Args:
        filename (str): The fully qualified name of the JSON file to read.

    Returns:
        dict: Parsed JSON data.
    """
    with json_data_file.open("r", encoding="utf-8") as file:
        data = json.load(file)

    return data


# Create a new session and load initial data
with TestingSessionLocal() as session:
    load_initial_data(session)
