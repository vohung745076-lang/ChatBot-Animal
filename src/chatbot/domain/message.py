"""Thực thể tin nhắn bất biến trong hệ thống VetChatbot."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """Đại diện cho một lượt phát biểu trong hội thoại tư vấn thú y."""
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"human", "ai"}:
            raise ValueError("Role chỉ được là 'human' hoặc 'ai'")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("Nội dung tin nhắn không được để trống")
