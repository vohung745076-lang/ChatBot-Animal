"""Kiểm tra định dạng khóa Google Gemini API."""
from src.chatbot.domain.errors import InvalidApiKey


def validate_api_key(api_key: str) -> str:
    """Xác thực định dạng Google Gemini API Key an toàn."""
    if not isinstance(api_key, str):
        raise InvalidApiKey("Khóa API phải là chuỗi ký tự")
    clean = api_key.strip()
    if len(clean) < 20 or len(clean) > 150:
        raise InvalidApiKey("Độ dài khóa API không hợp lệ (từ 20 đến 150 ký tự)")
    if any(c.isspace() for c in clean):
        raise InvalidApiKey("Khóa API không được chứa khoảng trắng")
    if not clean.isascii() or not clean.isprintable():
        raise InvalidApiKey("Khóa API chỉ được chứa các ký tự ASCII in được")
    return clean
