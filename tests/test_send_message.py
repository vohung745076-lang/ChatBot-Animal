"""Kiểm thử ca sử dụng gửi tin nhắn tư vấn thú y."""
import pytest
from src.chatbot.application.send_message import send_message
from src.chatbot.domain.errors import ApiKeyMissing
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository


def test_send_message_success():
    repo = FakeMemoryRepository()
    model = FakeChatModel("Thuốc Amoxicillin 15% dạng hỗn dịch tiêm")
    store = FakeApiKeyStore("AIzaSyFakeKey1234567890")
    reply = send_message(repo, model, store, "System prompt", 5, "session-12345", "Tư vấn thuốc")
    assert reply == "Thuốc Amoxicillin 15% dạng hỗn dịch tiêm"
    assert len(repo.get("session-12345")) == 2


def test_send_message_missing_key():
    repo = FakeMemoryRepository()
    model = FakeChatModel()
    store = FakeApiKeyStore("")
    with pytest.raises(ApiKeyMissing):
        send_message(repo, model, store, "Sys", 5, "session-12345", "Tư vấn")
    assert len(repo.get("session-12345")) == 0
