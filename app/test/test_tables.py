from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)

def test_create_table():
    response = client.post("/tables/", json={
        "name": "Test Table",
        "seats": 4,
        "location": "Test Zone"
    })
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Test Table"
    assert data["seats"] == 4

def test_get_tables():
    response = client.get("/tables/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)