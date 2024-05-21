import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))
from src.main import app
from fastapi.testclient import TestClient


client = TestClient(app)


def test_companies():
    response = client.get("/companies")
    assert response.status_code == 401
