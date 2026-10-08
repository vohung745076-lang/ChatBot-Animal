"""Kiểm thử thuật toán cắt gọt lịch sử hội thoại."""
import pytest
from src.chatbot.domain.message import Message
from src.chatbot.domain.trim_history import trim_history


def test_trim_history_empty():
    assert trim_history([], 5) == []


def test_trim_history_fewer_than_limit():
    msgs = [Message("human", "Hỏi liều Amoxicillin"), Message("ai", "10mg/kg")]
    assert trim_history(msgs, 5) == msgs


def test_trim_history_exceeding_limit():
    msgs = [Message("human", f"Câu hỏi {i}") for i in range(10)]
    trimmed = trim_history(msgs, 3)
    assert len(trimmed) == 3
    assert trimmed[0].content == "Câu hỏi 7"
    assert trimmed[2].content == "Câu hỏi 9"


def test_trim_history_invalid_limit():
    with pytest.raises(ValueError):
        trim_history([], 0)
