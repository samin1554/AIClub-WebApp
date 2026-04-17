def test_create_message(client):
    resp = client.post("/api/v1/sackbot/messages", json={
        "trigger": "welcome",
        "message": "Hey! Welcome to AI Club. I'm Sackbot!",
        "priority": "high",
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["trigger"] == "welcome"
    assert data["priority"] == "high"
    assert data["is_enabled"] is True
    assert data["context"] is None


def test_create_contextual_message(client):
    resp = client.post("/api/v1/sackbot/messages", json={
        "trigger": "contextual",
        "context": "ideas",
        "message": "Got an idea? Submit it and let the team vote!",
        "priority": "medium",
    })
    assert resp.status_code == 201
    assert resp.json()["data"]["context"] == "ideas"


def test_invalid_trigger(client):
    resp = client.post("/api/v1/sackbot/messages", json={
        "trigger": "random_unknown",
        "message": "Should fail",
    })
    assert resp.status_code == 422


def test_invalid_priority(client):
    resp = client.post("/api/v1/sackbot/messages", json={
        "trigger": "welcome",
        "message": "Should fail",
        "priority": "urgent",
    })
    assert resp.status_code == 422


def test_list_messages(client):
    client.post("/api/v1/sackbot/messages", json={"trigger": "welcome", "message": "Hi!"})
    client.post("/api/v1/sackbot/messages", json={"trigger": "encouragement", "message": "Great job!"})
    resp = client.get("/api/v1/sackbot/messages")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2


def test_get_message_by_trigger(client):
    client.post("/api/v1/sackbot/messages", json={"trigger": "welcome", "message": "Welcome!"})
    client.post("/api/v1/sackbot/messages", json={"trigger": "encouragement", "message": "Keep going!"})

    resp = client.get("/api/v1/sackbot/message?trigger=welcome")
    assert resp.status_code == 200
    assert resp.json()["data"]["trigger"] == "welcome"


def test_get_message_context_match(client):
    client.post("/api/v1/sackbot/messages", json={
        "trigger": "contextual", "context": "projects", "message": "Check out what we built!"
    })
    client.post("/api/v1/sackbot/messages", json={
        "trigger": "contextual", "context": "ideas", "message": "Vote on ideas here!"
    })

    resp = client.get("/api/v1/sackbot/message?trigger=contextual&context=ideas")
    assert resp.json()["data"]["message"] == "Vote on ideas here!"


def test_get_message_priority(client):
    client.post("/api/v1/sackbot/messages", json={
        "trigger": "welcome", "message": "Low priority msg", "priority": "low"
    })
    client.post("/api/v1/sackbot/messages", json={
        "trigger": "welcome", "message": "High priority msg", "priority": "high"
    })

    # Should always pick from the high-priority group
    for _ in range(5):
        resp = client.get("/api/v1/sackbot/message?trigger=welcome")
        assert resp.json()["data"]["priority"] == "high"


def test_get_message_no_messages(client):
    resp = client.get("/api/v1/sackbot/message")
    assert resp.status_code == 404


def test_get_message_no_filter(client):
    client.post("/api/v1/sackbot/messages", json={"trigger": "welcome", "message": "Hi!"})
    resp = client.get("/api/v1/sackbot/message")
    assert resp.status_code == 200


def test_delete_message(client):
    create = client.post("/api/v1/sackbot/messages", json={"trigger": "welcome", "message": "Hi!"})
    msg_id = create.json()["data"]["id"]

    assert client.delete(f"/api/v1/sackbot/messages/{msg_id}").status_code == 204
    assert client.get("/api/v1/sackbot/messages").json()["data"] == []


def test_delete_not_found(client):
    assert client.delete("/api/v1/sackbot/messages/999").status_code == 404
