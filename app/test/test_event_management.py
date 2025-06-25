import pytest
from httpx import AsyncClient
from app.main import app

@pytest.mark.asyncio
async def test_create_event():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/events", json={
            "name": "Test Event",
            "location": "Test Location",
            "start_datetime": "2025-07-01T10:00:00+05:30",
            "end_datetime": "2025-07-01T12:00:00+05:30",
            "max_capacity": 2,
            "description": "A test event"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Test Event"

@pytest.mark.asyncio
async def test_register_attendee():
    # First, create an event
    async with AsyncClient(app=app, base_url="http://test") as ac:
        event_resp = await ac.post("/events", json={
            "name": "Reg Event",
            "location": "Test Location",
            "start_datetime": "2025-07-01T10:00:00+05:30",
            "end_datetime": "2025-07-01T12:00:00+05:30",
            "max_capacity": 1,
            "description": "A test event"
        })
        event_id = event_resp.json()["id"]

        # Register first attendee
        reg_resp = await ac.post(f"/events/{event_id}/register", json={
            "attendee_name": "Alice",
            "attendee_email": "alice@example.com"
        })
        assert reg_resp.status_code == 200

        # Try duplicate registration
        dup_resp = await ac.post(f"/events/{event_id}/register", json={
            "attendee_name": "Alice",
            "attendee_email": "alice@example.com"
        })
        assert dup_resp.status_code == 400  # or your error code

        # Try overbooking
        overbook_resp = await ac.post(f"/events/{event_id}/register", json={
            "attendee_name": "Bob",
            "attendee_email": "bob@example.com"
        })
        assert overbook_resp.status_code == 400  # or your error code

@pytest.mark.asyncio
async def test_attendee_pagination():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Create event and register multiple attendees...
        # Then test pagination
        event_resp = await ac.post("/events", json={
            "name": "Paginate Event",
            "location": "Test Location",
            "start_datetime": "2025-07-01T10:00:00+05:30",
            "end_datetime": "2025-07-01T12:00:00+05:30",
            "max_capacity": 10,
            "description": "A test event"
        })
        event_id = event_resp.json()["id"]

        for i in range(5):
            await ac.post(f"/events/{event_id}/register", json={
                "attendee_name": f"User{i}",
                "attendee_email": f"user{i}@example.com"
            })

        resp = await ac.get(f"/events/{event_id}/attendees?limit=2&offset=0")
        assert resp.status_code == 200
        assert len(resp.json()) == 2

        resp2 = await ac.get(f"/events/{event_id}/attendees?limit=2&offset=2")
        assert resp2.status_code == 200
        assert len(resp2.json()) == 2

        resp3 = await ac.get(f"/events/{event_id}/attendees?limit=2&offset=4")
        assert resp3.status_code == 200
        assert len(resp3.json()) == 1
