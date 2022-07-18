import pytest
from main import api as starter
from fastapi.testclient import TestClient
import os


@pytest.fixture(autouse=True, scope="module")
def client():
   client = TestClient(starter)
   return client