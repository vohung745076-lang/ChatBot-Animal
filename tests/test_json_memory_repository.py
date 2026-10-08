"""Kiểm thử kho lưu trữ bộ nhớ JsonMemoryRepository."""
from src.chatbot.domain.message import Message
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository


def test_json_memory_repo_roundtrip(tmp_path):
    f = tmp_path / "memory.json"
    repo = JsonMemoryRepository(str(f))

    assert repo.get("sid-1") == []

    repo.append("sid-1", [Message("human", "Hỏi giá vaccine"), Message("ai", "Giá 150k")])
    history = repo.get("sid-1")
    assert len(history) == 2
    assert history[0].content == "Hỏi giá vaccine"
    assert history[1].content == "Giá 150k"

    repo.reset("sid-1")
    assert repo.get("sid-1") == []


def test_json_memory_repo_corrupt_file(tmp_path):
    f = tmp_path / "memory.json"
    f.write_text("{ corrupt json data ...", encoding="utf-8")
    repo = JsonMemoryRepository(str(f))
    # Phải tự phục hồi mà không crash
    assert repo.get("sid-1") == []
