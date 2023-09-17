from fastapi.testclient import TestClient

from app.application import app

client = TestClient(app)


def test_validate_csv_ok():
    
    response = client.post("/upload/", files={"csv_file": open("./test_data/valid_data.csv", "rb")})

    assert response.status_code == 200

    data = response.json()
    assert data["success"] is True
    assert data["errors"] == []

    assert data["expected_headers"] == ["year", "producer", "movie"]

    assert len(data["expected_headers"]) == len(data["data"][0])

    response = client.post("/upload/", files={"csv_file": open("./test_data/invalid_data.csv", "rb")})

    assert response.status_code == 422

    data = response.json()
    assert data["success"] is False
    assert data["errors"] != []