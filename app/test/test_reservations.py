from fastapi.testclient import TestClient
from app.main import app
from datetime import datetime, timedelta, timezone

client = TestClient(app)

def create_test_table():
    return client.post("/tables/", json={
        "name": "Test for Reservation",
        "seats": 2,
        "location": "Testing area"
    }).json()


def test_create_reservation():
    table = create_test_table()
    response = client.post("/reservations/", json={
        "customer_name": "John Doe",
        "table_id": table["id"],
        "reservation_time": datetime.now(timezone.utc).isoformat(),
        "duration_minutes": 60
    })
    assert response.status_code == 200
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["table_id"] == table["id"]


def test_conflict_reservation():
    table = create_test_table()
    start_time = datetime.now(timezone.utc).replace(microsecond=0)

    # Первая бронь
    client.post("/reservations/", json={
        "customer_name": "Alice",
        "reservation_time": start_time.isoformat(),
        "duration_minutes": 60
    })

    # Конфликтующая бронь
    response = client.post("/reservations/", json={
        "customer_name": "Bob",
        "table_id": table["id"],
        "reservation_time": (start_time + timedelta(minutes=30)).isoformat(),
        "duration_minutes": 60
    })
    assert response.status_code == 400
    assert "Table already booked" in response.json()["detail"]