"""Port quản lý và lưu trữ API Key."""
from abc import ABC, abstractmethod


class ApiKeyStore(ABC):
    """Giao diện trừu tượng cho nơi lưu trữ khóa bí mật API."""

    @abstractmethod
    def is_configured(self) -> bool:
        """Kiểm tra xem khóa đã được cấu hình hay chưa."""
        pass

    @abstractmethod
    def get(self) -> str:
        """Lấy giá trị khóa API hiện hành."""
        pass

    @abstractmethod
    def save(self, api_key: str) -> None:
        """Lưu khóa API mới một cách an toàn."""
        pass
