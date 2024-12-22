from collections.abc import Generator

import pytest_asyncio
from fastapi.testclient import TestClient


@pytest_asyncio.fixture(scope="session")
def client(request) -> Generator[TestClient]:
    """
    Fixture to create a TestClient with an optional mock for `get_current_user`.

    Args:
        request: The pytest request object used to access fixture parameters.

    Returns:
        TestClient: The FastAPI test client instance configured for the test.
    """
    # it's important to have this here, as it trigger the whole app initialization breaking console scripts
    from app.main import app

    with TestClient(
        app,
        headers={
            "Content-Language": "en",
        },
    ) as c:
        yield c
