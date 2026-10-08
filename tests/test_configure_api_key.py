"""Kiểm thử ca sử dụng lưu khóa API."""
from src.chatbot.application.configure_api_key import configure_api_key
from tests.fakes.fake_api_key_store import FakeApiKeyStore


def test_configure_api_key_success():
    store = FakeApiKeyStore("")
    assert not store.is_configured()
    configure_api_key(store, "AIzaSyDummyValidGeminiApiKey12345")
    assert store.is_configured()
    assert store.get() == "AIzaSyDummyValidGeminiApiKey12345"
