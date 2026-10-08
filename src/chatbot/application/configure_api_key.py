"""Ca sử dụng lưu khóa API từ người dùng."""
from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def configure_api_key(store: ApiKeyStore, raw_key: str) -> None:
    """Xác thực và lưu khóa API mới."""
    valid_key = validate_api_key(raw_key)
    store.save(valid_key)
