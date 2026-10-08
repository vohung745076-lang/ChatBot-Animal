"""Kho lưu trữ lịch sử hội thoại dạng JSON an toàn với luồng (Thread-safe)."""
import json
import threading
import time
from pathlib import Path
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.infrastructure.atomic_write_json import atomic_write_json


class JsonMemoryRepository(MemoryRepository):
    """Quản lý các phiên hội thoại trong file memory.json."""

    def __init__(self, file_path: str = "memory.json") -> None:
        self.file_path = file_path
        self._lock = threading.Lock()

    def _read_all(self) -> dict:
        path = Path(self.file_path)
        if not path.exists() or not path.is_file():
            return {}
        try:
            content = path.read_text(encoding="utf-8").strip()
            return json.loads(content) if content else {}
        except Exception:
            corrupt = path.parent / f"memory.json.corrupt-{int(time.time())}"
            path.rename(corrupt)
            return {}

    def get(self, session_id: str) -> list[Message]:
        with self._lock:
            data = self._read_all()
            raw_msgs = data.get(session_id, [])
            return [Message(m["role"], m["content"]) for m in raw_msgs]

    def append(self, session_id: str, messages: list[Message]) -> None:
        with self._lock:
            data = self._read_all()
            if session_id not in data:
                data[session_id] = []
            for m in messages:
                data[session_id].append({"role": m.role, "content": m.content})
            atomic_write_json(self.file_path, data)

    def reset(self, session_id: str) -> None:
        with self._lock:
            data = self._read_all()
            if session_id in data:
                data.pop(session_id, None)
                atomic_write_json(self.file_path, data)
