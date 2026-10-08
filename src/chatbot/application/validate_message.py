"""Kiểm tra nội dung câu hỏi tư vấn hàng hóa thú y."""
from src.chatbot.domain.errors import InvalidMessage


def validate_message(text: str) -> str:
    """Xác thực câu hỏi tư vấn thú y không rỗng và không vượt quá 4000 ký tự."""
    if not isinstance(text, str):
        raise InvalidMessage("Nội dung câu hỏi phải là chuỗi ký tự")
    clean = text.strip()
    if not clean:
        raise InvalidMessage("Nội dung câu hỏi tư vấn không được để trống")
    if len(clean) > 4000:
        raise InvalidMessage("Nội dung câu hỏi quá dài (tối đa 4000 ký tự)")
    return clean
