from fastapi.testclient import TestClient
from main import app
from unittest.mock import AsyncMock

client = TestClient(app)

def test_create_reservation(monkeypatch):
    # Create an AsyncMock for MongoRepository
    class DummyMongo:
        async def create(self, *args, **kwargs):
            return {
                "reservation_id": "123e4567-e89b-12d3-a456-426614174000",
                "customer_name": "John Doe",
                "guest_name": "John Doe",
                "room_type": "A-101",
                "arrival_date": "2025-08-01",
                "nights": 3,
                "room_id": "A",
                "hotel_id": 101,
                "room_count": 1,
                "created_at": "2025-07-15T22:14:18.379791+00:00",
                "_id": "someid"
            }

    # Patch app.state.mongo with DummyMongo instance
    app.state.mongo = DummyMongo()

    payload = {
        "customer_name": "John Doe",
        "guest_name": "John Doe",
        "room_type": "A-101",
        "arrival_date": "2025-08-01",
        "hotel_id": 101,
        "room_id": "A",
        "nights": 3,
        "room_count": 1
    }

    response = client.post("/api/v1/reservation/make", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "reservation_id" in data
