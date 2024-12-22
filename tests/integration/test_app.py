from fastapi.testclient import TestClient


def test_index_endpoint(client: TestClient):
    response = client.get("/")

    assert response.raise_for_status()
    assert response.json() == {"message": "Hello World!"}


def test_health_endpoint(client: TestClient):
    response = client.get("/monitoring/health")

    assert response.raise_for_status()
    assert response.json() == {"status": "healthy"}
