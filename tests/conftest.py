from app.config.database import get_session
from app.main import app
from tests.db_session import override_get_db

pytest_plugins = ("tests.fixtures",)


# Override dependency in the app with the test dependency
app.dependency_overrides[get_session] = override_get_db
