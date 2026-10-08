"""Port mô hình ngôn ngữ tương tác."""
from abc import ABC, abstractmethod
from src.chatbot.domain.message import Message


class ChatModel(ABC):
    """Giao diện trừu tượng gọi mô hình AI sinh câu trả lời tư vấn."""

    @abstractmethod
    def reply(
        self,
        system_prompt: str,
        history: list[Message],
        user_text: str
    ) -> str:
        """Sinh phản hồi tư vấn hàng hóa thú y từ mô hình AI."""
        pass
