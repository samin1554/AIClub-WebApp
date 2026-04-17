def test_create_member(client):
    resp = client.post("/api/v1/members", json={
        "display_name": "Alice",
        "bio": "AI enthusiast",
        "skills": ["python", "pytorch"],
        "role": "lead",
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["display_name"] == "Alice"
    assert data["role"] == "lead"
    assert "python" in data["skills"]


def test_list_members(client):
    client.post("/api/v1/members", json={"display_name": "Alice"})
    client.post("/api/v1/members", json={"display_name": "Bob"})
    resp = client.get("/api/v1/members")
    assert resp.status_code == 200
    assert len(resp.json()["data"]) == 2
    assert resp.json()["meta"]["pagination"]["total"] == 2


def test_get_member(client):
    create = client.post("/api/v1/members", json={"display_name": "Alice"})
    member_id = create.json()["data"]["id"]
    resp = client.get(f"/api/v1/members/{member_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["display_name"] == "Alice"


def test_update_member(client):
    create = client.post("/api/v1/members", json={"display_name": "Alice"})
    member_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/members/{member_id}", json={"bio": "Updated bio"})
    assert resp.status_code == 200
    assert resp.json()["data"]["bio"] == "Updated bio"


def test_filter_by_role(client):
    client.post("/api/v1/members", json={"display_name": "Alice", "role": "lead"})
    client.post("/api/v1/members", json={"display_name": "Bob", "role": "member"})
    resp = client.get("/api/v1/members?role=lead")
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["display_name"] == "Alice"


def test_filter_by_skill(client):
    client.post("/api/v1/members", json={"display_name": "Alice", "skills": ["python", "react"]})
    client.post("/api/v1/members", json={"display_name": "Bob", "skills": ["go", "rust"]})
    resp = client.get("/api/v1/members?skill=python")
    assert len(resp.json()["data"]) == 1
    assert resp.json()["data"][0]["display_name"] == "Alice"


def test_search_members(client):
    client.post("/api/v1/members", json={"display_name": "Alice Smith"})
    client.post("/api/v1/members", json={"display_name": "Bob Jones"})
    resp = client.get("/api/v1/members?search=alice")
    assert len(resp.json()["data"]) == 1


def test_member_not_found(client):
    assert client.get("/api/v1/members/999").status_code == 404
    assert client.patch("/api/v1/members/999", json={"bio": "X"}).status_code == 404


def test_pagination(client):
    for i in range(5):
        client.post("/api/v1/members", json={"display_name": f"Member {i}"})
    resp = client.get("/api/v1/members?page=1&limit=2")
    body = resp.json()
    assert len(body["data"]) == 2
    assert body["meta"]["pagination"]["total"] == 5
    assert body["meta"]["pagination"]["totalPages"] == 3
    assert body["meta"]["pagination"]["hasNext"] is True
