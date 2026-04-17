from unittest.mock import AsyncMock, patch, MagicMock
import pytest


MOCK_GROQ_PROMPT = {
    "choices": [{"message": {"content": "A lone developer stares at their screen at 3am, surrounded by empty coffee cups, debugging a mysterious recursion error that only appears in production."}}]
}


def mock_groq_post():
    mock_response = MagicMock()
    mock_response.status_code = 200
    mock_response.json.return_value = MOCK_GROQ_PROMPT
    return AsyncMock(return_value=mock_response)


@pytest.fixture(autouse=True)
def set_groq_key():
    import app.config as config_module
    config_module.settings.GROQ_API_KEY = "test-key-123"
    yield
    config_module.settings.GROQ_API_KEY = ""


def test_generate_prompt_defaults(client):
    with patch("app.services.prompt_lab_service.httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        resp = client.post("/api/v1/prompt-lab/generate", json={"topic": "debugging at 3am"})
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert "prompt" in data
        assert len(data["prompt"]) > 0
        assert data["topic"] == "debugging at 3am"
        assert data["style"] == "casual"
        assert data["mood"] == "neutral"
        assert data["length"] == "medium"


def test_generate_with_all_options(client):
    with patch("app.services.prompt_lab_service.httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        resp = client.post("/api/v1/prompt-lab/generate", json={
            "topic": "machine learning",
            "style": "technical",
            "mood": "serious",
            "length": "detailed",
        })
        assert resp.status_code == 200
        data = resp.json()["data"]
        assert data["style"] == "technical"
        assert data["mood"] == "serious"
        assert data["length"] == "detailed"


def test_generate_funny_creative(client):
    with patch("app.services.prompt_lab_service.httpx.AsyncClient") as mock_cls:
        mock_cls.return_value.__aenter__ = AsyncMock(return_value=MagicMock(post=mock_groq_post()))
        mock_cls.return_value.__aexit__ = AsyncMock(return_value=False)

        resp = client.post("/api/v1/prompt-lab/generate", json={
            "topic": "AI taking over the world",
            "style": "creative",
            "mood": "funny",
            "length": "short",
        })
        assert resp.status_code == 200


def test_generate_no_api_key(client):
    import app.config as config_module
    config_module.settings.GROQ_API_KEY = ""
    resp = client.post("/api/v1/prompt-lab/generate", json={"topic": "anything"})
    assert resp.status_code == 503


def test_invalid_style(client):
    resp = client.post("/api/v1/prompt-lab/generate", json={"topic": "test", "style": "sarcastic"})
    assert resp.status_code == 422


def test_invalid_mood(client):
    resp = client.post("/api/v1/prompt-lab/generate", json={"topic": "test", "mood": "angry"})
    assert resp.status_code == 422


def test_invalid_length(client):
    resp = client.post("/api/v1/prompt-lab/generate", json={"topic": "test", "length": "very-long"})
    assert resp.status_code == 422
