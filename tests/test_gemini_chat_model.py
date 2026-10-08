"""Kiểm thử tích hợp GeminiChatModel với mock requests."""
from unittest.mock import MagicMock, patch
import pytest
from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.infrastructure.gemini_chat_model import GeminiChatModel
from tests.fakes.fake_api_key_store import FakeApiKeyStore


def create_model(model_name: str = "gemini-3.5-flash") -> tuple[GeminiChatModel, FakeApiKeyStore]:
    store = FakeApiKeyStore("dummy_mock_gemini_key_12345")
    settings = Settings(
        gemini_api_key="dummy_mock_gemini_key_12345",
        gemini_model=model_name,
        gemini_temperature=0.2,
        gemini_timeout=10,
        host="127.0.0.1",
        port=2610,
        memory_file="memory.json",
        max_messages=6,
        system_prompt_file="system-prompt.txt",
    )
    return GeminiChatModel(settings, store), store


def test_gemini_reply_success():
    model, _ = create_model()
    mock_res = MagicMock()
    mock_res.ok = True
    mock_res.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Phản hồi thú y mẫu"}]}}]
    }
    with patch("requests.post", return_value=mock_res) as mock_post:
        ans = model.reply("System prompt", [Message("human", "Hỏi bệnh")], "Gà bị hen")
        assert ans == "Phản hồi thú y mẫu"
        assert mock_post.called
        headers = mock_post.call_args.kwargs["headers"]
        assert "Authorization" not in headers
        assert headers["x-goog-api-key"] == "dummy_mock_gemini_key_12345"


def test_gemini_model_fallback_on_404():
    model, _ = create_model("gemini-old-model")
    mock_404 = MagicMock(ok=False, status_code=404)
    mock_404.json.return_value = {"error": {"message": "models/gemini-old-model not found"}}
    mock_200 = MagicMock(ok=True)
    mock_200.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Phản hồi fallback"}]}}]
    }
    with patch("requests.post", side_effect=[mock_404, mock_200]) as mock_post:
        ans = model.reply("Prompt", [], "Test")
        assert ans == "Phản hồi fallback"
        assert mock_post.call_count == 2


def test_gemini_model_fallback_on_503():
    model, _ = create_model("gemini-busy-model")
    mock_503 = MagicMock(ok=False, status_code=503)
    mock_503.json.return_value = {"error": {"message": "High demand spikes"}}
    mock_200 = MagicMock(ok=True)
    mock_200.json.return_value = {
        "candidates": [{"content": {"parts": [{"text": "Phản hồi qua model dự phòng"}]}}]
    }
    with patch("requests.post", side_effect=[mock_503, mock_200]) as mock_post:
        ans = model.reply("Prompt", [], "Test")
        assert ans == "Phản hồi qua model dự phòng"
        assert mock_post.call_count == 2


def test_gemini_error_handling():
    model, _ = create_model()
    mock_res = MagicMock()
    mock_res.ok = False
    mock_res.status_code = 401
    mock_res.json.return_value = {"error": {"message": "API_KEY_INVALID"}}
    mock_res.text = "API_KEY_INVALID"
    with patch("requests.post", return_value=mock_res):
        with pytest.raises(UpstreamError) as exc_info:
            model.reply("Prompt", [], "Test")
        assert exc_info.value.status == 401
