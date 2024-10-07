from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def setup_function():
    """
    Runs before each test
    """
    pass

def test_ping():
    """
    This test just makes sure normal routes work
    """
    response = client.get("/V1/ping")
    assert response.status_code == 200
    assert response.json() == {"status": "success"}
