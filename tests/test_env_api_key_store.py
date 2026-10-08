"""Kiểm thử kho lưu trữ EnvApiKeyStore."""
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore


def test_env_api_key_store(tmp_path):
    f = tmp_path / ".env"
    f.write_text("PORT=2610\n", encoding="utf-8")
    store = EnvApiKeyStore(str(f))

    assert not store.is_configured()
    assert store.get() == ""

    store.save("AIzaSyMyNewKey123456789")
    assert store.is_configured()
    assert store.get() == "AIzaSyMyNewKey123456789"

    # Kiểm tra các dòng khác không bị xóa
    content = f.read_text(encoding="utf-8")
    assert "PORT=2610" in content
    assert "GEMINI_API_KEY=AIzaSyMyNewKey123456789" in content
