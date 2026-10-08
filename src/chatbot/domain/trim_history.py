"""Thuật toán cắt gọt lịch sử hội thoại tư vấn thú y."""
from src.chatbot.domain.message import Message


def trim_history(messages: list[Message], limit: int) -> list[Message]:
    """Trả về tối đa `limit` tin nhắn gần nhất mà không làm thay đổi thứ tự."""
    if limit <= 0:
        raise ValueError("Limit phải lớn hơn 0")
    if not messages:
        return []
    return list(messages[-limit:])
