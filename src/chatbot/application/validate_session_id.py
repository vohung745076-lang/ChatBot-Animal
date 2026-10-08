"""Kiểm tra tính hợp lệ của mã phiên hội thoại."""
import re
from src.chatbot.domain.errors import InvalidSession

SESSION_REGEX = re.compile(r"^[A-Za-z0-9-]{8,64}$")


def validate_session_id(session_id: str) -> str:
    """Xác thực session_id gồm từ 8 đến 64 ký tự an toàn."""
    if not isinstance(session_id, str) or not SESSION_REGEX.match(session_id.strip()):
        raise InvalidSession("Mã phiên hội thoại không hợp lệ (cần từ 8-64 ký tự hợp lệ)")
    return session_id.strip()
