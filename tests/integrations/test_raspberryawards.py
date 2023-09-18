import os
from fastapi.testclient import TestClient
import pytest

filename = os.path.basename(__file__)
dirname = os.path.dirname(__file__)


def test_validate_csv_success(client: TestClient):

    response = client.post("/upload/", files={"file":open(dirname+"/test_data/valid_data.csv", "rb")})

    assert response.status_code == 200
    assert response.is_error == False
    assert response.is_success == True

    data = response.json()

def test_validate_csv_fail(client: TestClient):
    
    response = client.post("/upload/", files={"csv_file": open(dirname+"/test_data/invalid_data.csv", "rb")})

    assert response.status_code == 422
    assert response.is_error == True
    assert response.is_success == False
    
    response = client.post("/upload/", files={"csv_file": open(dirname+"/test_data/invalid_type.txt", "rb")})

    assert response.status_code == 422
    assert response.is_error == True
    assert response.is_success == False
    