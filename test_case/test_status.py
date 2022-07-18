import pytest
from fastapi.testclient import TestClient
from main import api

client = TestClient(api)
#@pytest.mark.unit
def test_get(client):
    r = client.get("/status")
    assert r.status_code == 200
    assert r.json() == 1
    