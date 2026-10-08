"""Ghi dữ liệu JSON nguyên tử chuẩn UTF-8."""
import json
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


def atomic_write_json(file_path: str, data: dict) -> None:
    """Chuyển đổi dữ liệu sang chuỗi JSON và ghi nguyên tử."""
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    atomic_write_text(file_path, serialized)
