"""Hàm nạp và kiểm tra tính hợp lệ của cấu hình từ file .env."""
import os
from pathlib import Path
from dotenv import dotenv_values
from src.chatbot.config.settings import Settings
from src.chatbot.config.settings_error import SettingsError


def load_settings(env_path: str = ".env") -> Settings:
    """Nạp cấu hình từ file .env và biến môi trường hệ thống."""
    vals = {}
    path = Path(env_path)
    if path.exists() and path.is_file():
        vals = dotenv_values(dotenv_path=env_path)

    def get_val(key: str, default: str) -> str:
        return vals.get(key) or os.environ.get(key) or default

    api_key = get_val("GEMINI_API_KEY", "").strip()
    model = get_val("GEMINI_MODEL", "gemini-3.5-flash").strip()
    if not model:
        raise SettingsError("GEMINI_MODEL không được để trống")

    raw_temp = get_val("GEMINI_TEMPERATURE", "0.2")
    try:
        temp = float(raw_temp)
        if not (0.0 <= temp <= 2.0):
            raise ValueError()
    except ValueError:
        raise SettingsError("GEMINI_TEMPERATURE phải là số thực từ 0.0 đến 2.0")

    raw_timeout = get_val("GEMINI_TIMEOUT", "30")
    try:
        timeout = int(raw_timeout)
        if not (1 <= timeout <= 300):
            raise ValueError()
    except ValueError:
        raise SettingsError("GEMINI_TIMEOUT phải là số nguyên từ 1 đến 300")

    host = get_val("HOST", "127.0.0.1").strip()
    if host not in {"127.0.0.1", "localhost", "0.0.0.0"}:
        raise SettingsError("HOST chỉ chấp nhận 127.0.0.1, localhost hoặc 0.0.0.0")

    raw_port = get_val("PORT", "2610")
    try:
        port = int(raw_port)
        if not (1024 <= port <= 65535):
            raise ValueError()
    except ValueError:
        raise SettingsError("PORT phải là số nguyên từ 1024 đến 65535")

    raw_max = get_val("MAX_MESSAGES", "6")
    try:
        max_msg = int(raw_max)
        if not (1 <= max_msg <= 50):
            raise ValueError()
    except ValueError:
        raise SettingsError("MAX_MESSAGES phải là số nguyên từ 1 đến 50")

    memory_file = get_val("MEMORY_FILE", "memory.json").strip()
    prompt_file = get_val("SYSTEM_PROMPT_FILE", "system-prompt.txt").strip()

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        gemini_temperature=temp,
        gemini_timeout=timeout,
        host=host,
        port=port,
        memory_file=memory_file,
        max_messages=max_msg,
        system_prompt_file=prompt_file,
    )
