"""Port lưu trữ lịch sử hội thoại."""
from abc import ABC, abstractmethod
from src.chatbot.domain.message import Message


class MemoryRepository(ABC):
    """Giao diện trừu tượng cho kho lưu trữ bộ nhớ phiên."""

    @abstractmethod
    def get(self, session_id: str) -> list[Message]:
        """Lấy danh sách tin nhắn theo session_id."""
        pass

    @abstractmethod
    def append(self, session_id: str, messages: list[Message]) -> None:
        """Ghi nối tiếp danh sách tin nhắn vào session."""
        pass

    @abstractmethod
    def reset(self, session_id: str) -> None:
        """Xóa toàn bộ lịch sử của session."""
        pass
