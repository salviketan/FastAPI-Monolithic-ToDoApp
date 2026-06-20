from fastapi.testclient import TestClient
from httpx._models import Response

from app.main import app

client = TestClient(app)


def test_get_tasks(mock_db_session) -> None:
    response: Response = client.get("api/v1/tasks")

    assert response.status_code == 200
