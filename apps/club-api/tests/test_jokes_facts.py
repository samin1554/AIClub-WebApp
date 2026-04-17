def test_create_joke(client):
    resp = client.post("/api/v1/jokes-facts", json={"content": "Why do programmers prefer dark mode? Light attracts bugs!", "type": "joke"})
    assert resp.status_code == 201
    data = resp.json()["data"]
    assert data["type"] == "joke"
    assert data["is_active"] is True


def test_create_fact(client):
    resp = client.post("/api/v1/jokes-facts", json={"content": "Python was named after Monty Python, not the snake.", "type": "fact"})
    assert resp.status_code == 201
    assert resp.json()["data"]["type"] == "fact"


def test_list_all(client):
    client.post("/api/v1/jokes-facts", json={"content": "Joke 1", "type": "joke"})
    client.post("/api/v1/jokes-facts", json={"content": "Fact 1", "type": "fact"})
    client.post("/api/v1/jokes-facts", json={"content": "Joke 2", "type": "joke"})

    resp = client.get("/api/v1/jokes-facts")
    assert len(resp.json()["data"]) == 3
    assert resp.json()["meta"]["pagination"]["total"] == 3


def test_filter_by_type(client):
    client.post("/api/v1/jokes-facts", json={"content": "Joke", "type": "joke"})
    client.post("/api/v1/jokes-facts", json={"content": "Fact", "type": "fact"})

    jokes = client.get("/api/v1/jokes-facts?type=joke").json()["data"]
    facts = client.get("/api/v1/jokes-facts?type=fact").json()["data"]

    assert len(jokes) == 1 and jokes[0]["type"] == "joke"
    assert len(facts) == 1 and facts[0]["type"] == "fact"


def test_invalid_type_filter(client):
    resp = client.get("/api/v1/jokes-facts?type=meme")
    assert resp.status_code == 400


def test_get_random(client):
    client.post("/api/v1/jokes-facts", json={"content": "Joke A", "type": "joke"})
    client.post("/api/v1/jokes-facts", json={"content": "Joke B", "type": "joke"})

    resp = client.get("/api/v1/jokes-facts/random")
    assert resp.status_code == 200
    assert resp.json()["data"]["type"] == "joke"


def test_get_random_by_type(client):
    client.post("/api/v1/jokes-facts", json={"content": "Fact only", "type": "fact"})
    resp = client.get("/api/v1/jokes-facts/random?type=fact")
    assert resp.status_code == 200
    assert resp.json()["data"]["type"] == "fact"


def test_random_empty(client):
    resp = client.get("/api/v1/jokes-facts/random")
    assert resp.status_code == 404


def test_delete(client):
    create = client.post("/api/v1/jokes-facts", json={"content": "Delete me", "type": "joke"})
    item_id = create.json()["data"]["id"]

    assert client.delete(f"/api/v1/jokes-facts/{item_id}").status_code == 204
    assert client.get("/api/v1/jokes-facts").json()["meta"]["pagination"]["total"] == 0


def test_delete_not_found(client):
    assert client.delete("/api/v1/jokes-facts/999").status_code == 404


def test_pagination(client):
    for i in range(5):
        client.post("/api/v1/jokes-facts", json={"content": f"Joke {i}", "type": "joke"})

    resp = client.get("/api/v1/jokes-facts?page=1&limit=2")
    assert len(resp.json()["data"]) == 2
    assert resp.json()["meta"]["pagination"]["total"] == 5
    assert resp.json()["meta"]["pagination"]["hasNext"] is True
