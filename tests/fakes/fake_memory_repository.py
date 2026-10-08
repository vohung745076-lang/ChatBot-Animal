"""Fake implementation cho MemoryRepository phục vụ kiểm thử."""
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository


class FakeMemoryRepository(MemoryRepository):
    def __init__(self) -> None:
        self.data: dict[str, list[Message]] = {}

    def get(self, session_id: str) -> list[Message]:
        return list(self.data.get(session_id, []))

    def append(self, session_id: str, messages: list[Message]) -> None:
        if session_id not in self.data:
            self.data[session_id] = []
        self.data[session_id].extend(messages)

    def reset(self, session_id: str) -> None:
        self.data.pop(session_id, None)
