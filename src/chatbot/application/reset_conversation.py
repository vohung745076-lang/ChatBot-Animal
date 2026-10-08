"""Ca sử dụng làm mới cuộc trò chuyện."""
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.ports.memory_repository import MemoryRepository


def reset_conversation(repo: MemoryRepository, session_id: str) -> None:
    """Xác thực session_id và xóa lịch sử hội thoại."""
    valid_id = validate_session_id(session_id)
    repo.reset(valid_id)
