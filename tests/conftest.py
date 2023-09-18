from typing import Generator
from main import app
from fastapi.testclient import TestClient
import pytest

@pytest.fixture(scope="function")
def client() -> Generator:
    with TestClient(app) as c:
        yield c
    