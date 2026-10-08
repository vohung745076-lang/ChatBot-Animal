"""Kiểm thử unit test cho tầng cấu hình VetChatbot."""
import pytest
from src.chatbot.config.load_settings import load_settings
from src.chatbot.config.settings_error import SettingsError


def test_load_settings_defaults(tmp_path, monkeypatch):
    monkeypatch.delenv("GEMINI_API_KEY", raising=False)
    non_existent = tmp_path / ".env.none"
    s = load_settings(str(non_existent))
    assert s.gemini_model == "gemini-1.5-flash"
    assert s.host == "127.0.0.1"
    assert s.port == 2610
    assert s.gemini_temperature == 0.2
    assert s.gemini_api_key == ""


def test_load_settings_custom(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GEMINI_API_KEY=AIzaSyDummyTestKey1234567890\n"
        "GEMINI_MODEL=gemini-1.5-pro\n"
        "PORT=3000\n"
        "GEMINI_TEMPERATURE=0.7\n",
        encoding="utf-8"
    )
    s = load_settings(str(env_file))
    assert s.gemini_api_key == "AIzaSyDummyTestKey1234567890"
    assert s.gemini_model == "gemini-1.5-pro"
    assert s.port == 3000
    assert s.gemini_temperature == 0.7


def test_reject_invalid_host(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("HOST=192.168.1.100\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="HOST chỉ chấp nhận"):
        load_settings(str(env_file))


def test_accept_cloud_host(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("HOST=0.0.0.0\n", encoding="utf-8")
    s = load_settings(str(env_file))
    assert s.host == "0.0.0.0"


def test_reject_invalid_port(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=99999\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="PORT phải là số nguyên"):
        load_settings(str(env_file))


def test_reject_invalid_temperature(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GEMINI_TEMPERATURE=3.5\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="GEMINI_TEMPERATURE"):
        load_settings(str(env_file))
