"""Lớp cấu hình bất biến cho hệ thống VetChatbot (Google Gemini)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Chứa toàn bộ thông số vận hành của VetChatbot."""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    gemini_temperature: float = 0.2
    gemini_timeout: int = 30
    host: str = "127.0.0.1"
    port: int = 2610
    memory_file: str = "memory.json"
    max_messages: int = 6
    system_prompt_file: str = "system-prompt.txt"
