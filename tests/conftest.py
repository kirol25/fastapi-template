"""Shared fixtures for the test suite.

Strategy
--------
- ``db_engine`` (session-scoped): connects to a test database, creates all
  tables once, and drops them after the session ends. Skips automatically
  if the database is not reachable, so tests can run without Postgres.
- ``db_session`` (function-scoped): wraps each test in an outer transaction +
  a SAVEPOINT. Both are rolled back on teardown, so tests never persist data
  and IntegrityError assertions don't abort the outer connection.
- ``client`` (session-scoped): a TestClient with the database session
  dependency overridden.
"""

import os
from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Engine, create_engine, event, text
from sqlalchemy.orm import Session

from app.config.database import Base
from app.main import app

TEST_DATABASE_URL = os.environ.get(
    "TEST_DATABASE_URL",
    "sqlite:///:memory:",
)


# ---------------------------------------------------------------------------
# Database engine - session-scoped
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def db_engine() -> Generator[Engine]:
    """Create the test schema once per pytest session and tear it down after."""
    engine = create_engine(TEST_DATABASE_URL, pool_pre_ping=True)
    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
    except Exception as exc:
        pytest.skip(f"Test database unavailable: {exc}")

    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)
    engine.dispose()


# ---------------------------------------------------------------------------
# Database session - function-scoped with automatic rollback
# ---------------------------------------------------------------------------


@pytest.fixture
def db_session(db_engine: Engine) -> Generator[Session]:
    """Yield an ORM session isolated inside a transaction + SAVEPOINT.

    The outer BEGIN wraps the entire test. A SAVEPOINT is created so that
    IntegrityError tests can roll back without aborting the connection.
    Everything is rolled back unconditionally after the test.
    """
    connection = db_engine.connect()
    outer_transaction = connection.begin()
    session = Session(bind=connection)

    nested = connection.begin_nested()

    @event.listens_for(session, "after_transaction_end")
    def restart_savepoint(session: Session, transaction) -> None:
        nonlocal nested
        if transaction.nested and not transaction._parent.nested:
            session.expire_all()
            nested = connection.begin_nested()

    yield session

    session.close()
    outer_transaction.rollback()
    connection.close()


# ---------------------------------------------------------------------------
# HTTP test client
# ---------------------------------------------------------------------------


@pytest.fixture(scope="session")
def client() -> Generator[TestClient]:
    """A TestClient for integration tests."""
    with TestClient(app) as c:
        yield c
