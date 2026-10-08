"""Kiểm thử ca sử dụng làm mới cuộc trò chuyện."""
from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.domain.message import Message
from tests.fakes.fake_memory_repository import FakeMemoryRepository


def test_reset_conversation():
    repo = FakeMemoryRepository()
    sid = "session-12345"
    repo.append(sid, [Message("human", "Hỏi liều thuốc"), Message("ai", "Trả lời")])
    assert len(repo.get(sid)) == 2

    reset_conversation(repo, sid)
    assert len(repo.get(sid)) == 0
