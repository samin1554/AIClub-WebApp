def base_request(**kwargs):
    data = {
        "title": "Build a study tracker",
        "problem": "We need a way to track study sessions",
        "desired_outcome": "A simple web app to log hours",
    }
    data.update(kwargs)
    return data


def test_create_request(client):
    resp = client.post("/api/v1/requests", json=base_request())
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["title"] == "Build a study tracker"
    assert data["status"] == "new"
    assert data["priority"] == "medium"
    assert data["comment_count"] == 0


def test_create_with_requester_info(client):
    resp = client.post("/api/v1/requests", json=base_request(
        requester_name="Prof. Smith",
        requester_contact="smith@university.edu",
        constraints="Must be mobile-friendly",
    ))
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["requester_name"] == "Prof. Smith"
    assert data["constraints"] == "Must be mobile-friendly"


def test_list_requests(client):
    client.post("/api/v1/requests", json=base_request(title="Request 1"))
    client.post("/api/v1/requests", json=base_request(title="Request 2"))
    resp = client.get("/api/v1/requests")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2
    assert resp.json()["meta"]["pagination"]["total"] == 2


def test_get_request(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    resp = client.get(f"/api/v1/requests/{req_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Build a study tracker"


def test_update_status(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/requests/{req_id}", json={"status": "reviewing"})
    assert resp.status_code == 200
    assert resp.json()["data"]["status"] == "reviewing"


def test_update_priority_and_assign(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/requests/{req_id}", json={"priority": "high", "assigned_member_id": 5})
    assert resp.json()["data"]["priority"] == "high"
    assert resp.json()["data"]["assigned_member_id"] == 5


def test_invalid_status(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/requests/{req_id}", json={"status": "banana"})
    assert resp.status_code == 400


def test_invalid_priority(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/requests/{req_id}", json={"priority": "urgent"})
    assert resp.status_code == 400


def test_delete_request(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]
    assert client.delete(f"/api/v1/requests/{req_id}").status_code == 204
    assert client.get(f"/api/v1/requests/{req_id}").status_code == 404


def test_filter_by_status(client):
    client.post("/api/v1/requests", json=base_request(title="New one"))
    create2 = client.post("/api/v1/requests", json=base_request(title="Old one"))
    client.patch(f"/api/v1/requests/{create2.json()['data']['id']}", json={"status": "shipped"})

    resp = client.get("/api/v1/requests?status=shipped")
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["title"] == "Old one"


def test_filter_by_priority(client):
    client.post("/api/v1/requests", json=base_request(title="Normal"))
    create2 = client.post("/api/v1/requests", json=base_request(title="Urgent"))
    client.patch(f"/api/v1/requests/{create2.json()['data']['id']}", json={"priority": "high"})

    resp = client.get("/api/v1/requests?priority=high")
    assert len(resp.json()["data"]) == 1


def test_comments(client):
    create = client.post("/api/v1/requests", json=base_request())
    req_id = create.json()["data"]["id"]

    # Add comment
    resp = client.post(f"/api/v1/requests/{req_id}/comments", json={"member_id": 1, "body": "On it!"})
    assert resp.status_code == 201
    comment_id = resp.json()["data"]["id"]

    # List
    resp = client.get(f"/api/v1/requests/{req_id}/comments")
    assert len(resp.json()["data"]) == 1

    # comment_count increments
    resp = client.get(f"/api/v1/requests/{req_id}")
    assert resp.json()["data"]["comment_count"] == 1

    # Delete comment
    resp = client.delete(f"/api/v1/requests/{req_id}/comments/{comment_id}")
    assert resp.status_code == 204


def test_request_not_found(client):
    assert client.get("/api/v1/requests/999").status_code == 404
    assert client.patch("/api/v1/requests/999", json={"status": "new"}).status_code == 404
    assert client.delete("/api/v1/requests/999").status_code == 404
