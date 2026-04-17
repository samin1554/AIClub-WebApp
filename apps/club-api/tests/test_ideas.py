def test_create_idea(client):
    resp = client.post("/api/v1/ideas", json={
        "title": "AI Study Group",
        "pitch": "Weekly study sessions on ML papers",
        "tags": ["ml", "study"],
    })
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["title"] == "AI Study Group"
    assert data["vote_count"] == 0
    assert data["comment_count"] == 0


def test_list_ideas(client):
    client.post("/api/v1/ideas", json={"title": "Idea 1", "pitch": "Pitch 1"})
    client.post("/api/v1/ideas", json={"title": "Idea 2", "pitch": "Pitch 2"})
    resp = client.get("/api/v1/ideas")
    assert resp.status_code == 200
    body = resp.json()
    assert len(body["data"]) == 2
    assert body["meta"]["pagination"]["total"] == 2


def test_get_idea(client):
    create = client.post("/api/v1/ideas", json={"title": "Test", "pitch": "Test pitch"})
    idea_id = create.json()["data"]["id"]
    resp = client.get(f"/api/v1/ideas/{idea_id}")
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "Test"


def test_update_idea(client):
    create = client.post("/api/v1/ideas", json={"title": "Old", "pitch": "Old pitch"})
    idea_id = create.json()["data"]["id"]
    resp = client.patch(f"/api/v1/ideas/{idea_id}", json={"title": "New"})
    assert resp.status_code == 200
    assert resp.json()["data"]["title"] == "New"


def test_delete_idea(client):
    create = client.post("/api/v1/ideas", json={"title": "Del", "pitch": "Delete me"})
    idea_id = create.json()["data"]["id"]
    resp = client.delete(f"/api/v1/ideas/{idea_id}")
    assert resp.status_code == 204
    resp = client.get(f"/api/v1/ideas/{idea_id}")
    assert resp.status_code == 404


def test_vote_and_unvote(client):
    create = client.post("/api/v1/ideas", json={"title": "Vote test", "pitch": "Vote"})
    idea_id = create.json()["data"]["id"]

    # Vote
    resp = client.post(f"/api/v1/ideas/{idea_id}/vote", json={"member_id": 1})
    assert resp.status_code == 200
    assert resp.json()["data"]["vote_count"] == 1

    # Duplicate vote should fail
    resp = client.post(f"/api/v1/ideas/{idea_id}/vote", json={"member_id": 1})
    assert resp.status_code == 409

    # Second member votes
    resp = client.post(f"/api/v1/ideas/{idea_id}/vote", json={"member_id": 2})
    assert resp.json()["data"]["vote_count"] == 2

    # Unvote
    resp = client.delete(f"/api/v1/ideas/{idea_id}/vote?member_id=1")
    assert resp.status_code == 200
    assert resp.json()["data"]["vote_count"] == 1


def test_comments(client):
    create = client.post("/api/v1/ideas", json={"title": "Comment test", "pitch": "Comments"})
    idea_id = create.json()["data"]["id"]

    # Add comment
    resp = client.post(
        f"/api/v1/ideas/{idea_id}/comments",
        json={"member_id": 1, "body": "Great idea!"},
    )
    assert resp.status_code == 201
    comment_id = resp.json()["data"]["id"]

    # List comments
    resp = client.get(f"/api/v1/ideas/{idea_id}/comments")
    assert len(resp.json()["data"]) == 1

    # Delete comment
    resp = client.delete(f"/api/v1/ideas/{idea_id}/comments/{comment_id}")
    assert resp.status_code == 204


def test_idea_not_found(client):
    assert client.get("/api/v1/ideas/999").status_code == 404
    assert client.patch("/api/v1/ideas/999", json={"title": "X"}).status_code == 404
    assert client.delete("/api/v1/ideas/999").status_code == 404


def test_search_ideas(client):
    client.post("/api/v1/ideas", json={"title": "Machine Learning", "pitch": "ML stuff"})
    client.post("/api/v1/ideas", json={"title": "Web Dev", "pitch": "Frontend"})
    resp = client.get("/api/v1/ideas?search=Machine")
    assert len(resp.json()["data"]) == 1
