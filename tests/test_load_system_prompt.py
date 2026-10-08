"""Kiểm thử nạp file system prompt chuyên gia thú y."""
from src.chatbot.infrastructure.load_system_prompt import DEFAULT_VET_PROMPT, load_system_prompt


def test_load_system_prompt_fallback(tmp_path):
    non_existent = tmp_path / "system-prompt.txt"
    res = load_system_prompt(str(non_existent))
    assert res == DEFAULT_VET_PROMPT


def test_load_system_prompt_custom(tmp_path):
    f = tmp_path / "prompt.txt"
    f.write_text("Prompt thú y riêng", encoding="utf-8")
    res = load_system_prompt(str(f))
    assert res == "Prompt thú y riêng"
