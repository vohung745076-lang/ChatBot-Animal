"""Kiểm thử ghi tệp nguyên tử."""
from src.chatbot.infrastructure.atomic_write_json import atomic_write_json
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


def test_atomic_write_text(tmp_path):
    target = tmp_path / "sub" / "test.txt"
    atomic_write_text(str(target), "Nội dung kiểm thử")
    assert target.read_text(encoding="utf-8") == "Nội dung kiểm thử"


def test_atomic_write_json(tmp_path):
    target = tmp_path / "data.json"
    data = {"thuoc": "Amoxicillin", "lieu": "10mg/kg"}
    atomic_write_json(str(target), data)
    assert '"thuoc": "Amoxicillin"' in target.read_text(encoding="utf-8")
