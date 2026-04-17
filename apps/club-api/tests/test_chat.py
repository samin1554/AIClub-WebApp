from unittest.mock import AsyncMock, patch, MagicMock
import pytest


MOCK_GROQ_RESPONSE = {
    "choices": [{"message": {"content": "Hello! I'm the AI Club assistant. How can I help?"}}]
}


def mock_groq_post():
    """Returns a mock for httpx.AsyncClient.post that simulates Groq."""
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_GROQ_RESPONSE
    mock = AsyncMock(return_value=mock_response)
    return mock


@pytest.fixture(autouse=True)
def set_groq_key(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "test-key-123")
    # Re-create settings with the patched env var
    import app.config as config_module
    config_module.settings.GROQ_API_KEY = "test-key-123"
    yield
    config_module.settings.GROQ_API_KEY = ""


def test_send_message(client):
    with patch("app.services.chat_service.httpx.AsyncClient") as mock_client_cls:
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        resp = client.post("/api/v1/chat", json={"session_key": "session-abc", "message": "Hello"})
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["session_key"] == "session-abc"
        assert "assistant" in data["reply"].lower() or len(data["reply"]) > 0


def test_get_history(client):
    with patch("app.services.chat_service.httpx.AsyncClient") as mock_client_cls:
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        client.post("/api/v1/chat", json={"session_key": "session-xyz", "message": "Hi there"})

    resp = client.get("/api/v1/chat/session-xyz")
    assert resp.status_code == 200
    messages = resp.json()["data"]
    assert len(messages) == 2  # user + assistant
    assert messages[0]["role"] == "user"
    assert messages[1]["role"] == "assistant"


def test_get_history_empty_session(client):
    resp = client.get("/api/v1/chat/nonexistent-session")
    assert resp.status_code == 200
    assert resp.json()["data"] == []


def test_clear_session(client):
    with patch("app.services.chat_service.httpx.AsyncClient") as mock_client_cls:
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        client.post("/api/v1/chat", json={"session_key": "session-del", "message": "test"})

    # History exists
    assert len(client.get("/api/v1/chat/session-del").json()["data"]) == 2

    # Clear it
    resp = client.delete("/api/v1/chat/session-del")
    assert resp.status_code == 204

    # History gone
    assert client.get("/api/v1/chat/session-del").json()["data"] == []


def test_chatbot_no_api_key(client):
    import app.config as config_module
    config_module.settings.GROQ_API_KEY = ""
    resp = client.post("/api/v1/chat", json={"session_key": "s", "message": "hi"})
    assert resp.status_code == 503


def test_multiple_turns(client):
    with patch("app.services.chat_service.httpx.AsyncClient") as mock_client_cls:
        mock_client_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_client_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        client.post("/api/v1/chat", json={"session_key": "multi", "message": "Message 1"})
        client.post("/api/v1/chat", json={"session_key": "multi", "message": "Message 2"})

    resp = client.get("/api/v1/chat/multi")
    messages = resp.json()["data"]
    assert len(messages) == 4  # 2 user + 2 assistant
