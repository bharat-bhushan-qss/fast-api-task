import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from fastapi.testclient import TestClient
from src.main import app


client = TestClient(app)


def test_contacts():
    response = client.get("/contacts")
    assert response.status_code == 401
