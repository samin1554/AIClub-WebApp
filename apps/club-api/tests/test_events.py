from datetime import datetime, timedelta, timezone


def future_event(hours_from_now=24):
    now = datetime.now(timezone.utc)
    return {
        "title": "AI Workshop",
        "description": "Learn about neural networks",
        "starts_at": (now + timedelta(hours=hours_from_now)).isoformat(),
        "ends_at": (now + timedelta(hours=hours_from_now + 2)).isoformat(),
        "location": "Room 101",
    }


def test_create_event(client):
    resp = client.post("/api/v1/events", json=future_event())
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["title"] == "AI Workshop"
    assert data["rsvp_count"] == 0


def test_invalid_time_range(client):
    now = datetime.now(timezone.utc)
    resp = client.post("/api/v1/events", json={
        "title": "Bad Event",
        "starts_at": (now + timedelta(hours=5)).isoformat(),
        "ends_at": (now + timedelta(hours=3)).isoformat(),
    })
    assert resp.status_code == 400


def test_list_events(client):
    client.post("/api/v1/events", json=future_event(24))
    client.post("/api/v1/events", json=future_event(48))
    resp = client.get("/api/v1/events")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2


def test_get_event(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]
    resp = client.get(f"/api/v1/events/{event_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "AI Workshop"


def test_update_event(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/events/{event_id}", json={"title": "Updated Workshop"})
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Updated Workshop"


def test_delete_event(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]
    assert client.delete(f"/api/v1/events/{event_id}").status_code == 204
    assert client.get(f"/api/v1/events/{event_id}").status_code == 404


def test_rsvp_and_cancel(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]

    # RSVP
    resp = client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 1})
    assert resp.json()["data"]["rsvp_count"] == 1

    # Second RSVP (same user updates status)
    resp = client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 1, "status": "maybe"})
    assert resp.json()["data"]["rsvp_count"] == 0  # "maybe" doesn't count as going

    # Cancel
    resp = client.delete(f"/api/v1/events/{event_id}/rsvp?user_id=1")
    assert resp.status_code == 200


def test_rsvp_capacity(client):
    event_data = future_event()
    event_data["max_attendees"] = 1
    create = client.post("/api/v1/events", json=event_data)
    event_id = create.json()["data"]["id"]

    # First RSVP succeeds
    resp = client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 1})
    assert resp.status_code == 200

    # Second RSVP should fail (at capacity)
    resp = client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 2})
    assert resp.status_code == 409


def test_attendees(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]
    client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 1})
    client.post(f"/api/v1/events/{event_id}/rsvp", json={"user_id": 2})

    resp = client.get(f"/api/v1/events/{event_id}/attendees")
    assert len(resp.json()["data"]) == 2


def test_calendar_export(client):
    create = client.post("/api/v1/events", json=future_event())
    event_id = create.json()["data"]["id"]
    resp = client.get(f"/api/v1/events/{event_id}/calendar.ics")
    assert resp.status_code == 200
    assert "BEGIN:VCALENDAR" in resp.text
    assert "AI Workshop" in resp.text


def test_event_not_found(client):
    assert client.get("/api/v1/events/999").status_code == 404
