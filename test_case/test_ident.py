import pytest
from fastapi.testclient import TestClient
from main import api
import json

client = TestClient(api)

def test_identification_bob(client):
    response = client.get("/identification/bob/builder")
    assert response.status_code == 200
    assert response.json() == {
       "user_status": 1
    }


def test_identification_0(client):
    response = client.get("/identification/bo/builder")
    assert response.status_code == 200
    assert response.json() == {
       "user_status": 0
    }
