"""Ca sử dụng lấy trạng thái cấu hình khóa API."""
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def get_setup_status(store: ApiKeyStore) -> dict:
    """Trả về trạng thái đã cấu hình khóa hay chưa."""
    return {"configured": store.is_configured()}
