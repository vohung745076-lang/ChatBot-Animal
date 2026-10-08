"""Kiểm thử các hàm xác thực dữ liệu đầu vào."""
import pytest
from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import InvalidApiKey, InvalidMessage, InvalidSession


def test_validate_session_id_valid():
    assert validate_session_id("vet-session-12345") == "vet-session-12345"


def test_validate_session_id_invalid():
    with pytest.raises(InvalidSession):
        validate_session_id("short")
    with pytest.raises(InvalidSession):
        validate_session_id("invalid!@#$characters")


def test_validate_message_valid():
    assert validate_message(" Cho tôi hỏi liều thuốc ") == "Cho tôi hỏi liều thuốc"


def test_validate_message_invalid():
    with pytest.raises(InvalidMessage):
        validate_message("   ")
    with pytest.raises(InvalidMessage):
        validate_message("a" * 4001)


def test_validate_api_key_valid():
    key = "AIzaSyDummyValidGeminiApiKey12345"
    assert validate_api_key(key) == key


def test_validate_api_key_invalid():
    with pytest.raises(InvalidApiKey):
        validate_api_key("short_key")
    with pytest.raises(InvalidApiKey):
        validate_api_key("key with spaces in the middle 123456789")
