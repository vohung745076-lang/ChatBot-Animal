"""Kiểm thử ánh xạ lỗi từ Google Gemini API."""
from src.chatbot.infrastructure.map_gemini_error import map_gemini_error


def test_map_gemini_error_auth():
    err = Exception("API_KEY_INVALID: unauthenticated call")
    status, msg = map_gemini_error(err)
    assert status == 401
    assert "chính xác" in msg


def test_map_gemini_error_quota():
    err = Exception("RESOURCE_EXHAUSTED: 429 Quota exceeded")
    status, msg = map_gemini_error(err)
    assert status == 503
    assert "quá tải" in msg or "Hạn ngạch" in msg


def test_map_gemini_error_timeout():
    err = Exception("DEADLINE_EXCEEDED: timeout occurred")
    status, msg = map_gemini_error(err)
    assert status == 504
    assert "thời gian" in msg
