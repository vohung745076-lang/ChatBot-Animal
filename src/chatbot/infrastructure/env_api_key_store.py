"""Lưu trữ và đồng bộ Google Gemini API Key vào file .env."""
import os
from pathlib import Path
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


class EnvApiKeyStore(ApiKeyStore):
    """Cài đặt lưu khóa API vào file .env và cập nhật os.environ."""

    def __init__(self, env_path: str = ".env") -> None:
        self.env_path = env_path

    def is_configured(self) -> bool:
        return bool(self.get())

    def get(self) -> str:
        val = os.environ.get("GEMINI_API_KEY", "").strip()
        if val:
            return val
        path = Path(self.env_path)
        if path.exists() and path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
        return ""

    def save(self, api_key: str) -> None:
        clean = api_key.strip()
        lines = []
        path = Path(self.env_path)
        found = False
        if path.exists() and path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("GEMINI_API_KEY="):
                    lines.append(f"GEMINI_API_KEY={clean}")
                    found = True
                else:
                    lines.append(line)
        if not found:
            lines.append(f"GEMINI_API_KEY={clean}")
        atomic_write_text(self.env_path, "\n".join(lines) + "\n")
        os.environ["GEMINI_API_KEY"] = clean
