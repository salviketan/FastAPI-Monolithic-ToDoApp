from fastapi.testclient import TestClient
from httpx._models import Response
from main import app

client = TestClient(app)


def test_get_tasks(mock_db_session) -> None:
    response: Response = client.get("/task", skip=0, limit=100)

    assert response.status_code == 200
    # data  = response.json()
    # assert data["name"] = ""
