"""Fake implementation cho ApiKeyStore phục vụ kiểm thử."""
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


class FakeApiKeyStore(ApiKeyStore):
    def __init__(self, key: str = "") -> None:
        self._key = key

    def is_configured(self) -> bool:
        return bool(self._key)

    def get(self) -> str:
        return self._key

    def save(self, api_key: str) -> None:
        self._key = api_key
