"""Điểm khởi chạy máy chủ VetChatbot trên Windows 11."""
import sys
from src.chatbot.config.load_settings import load_settings
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore
from src.chatbot.infrastructure.gemini_chat_model import GeminiChatModel
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository
from src.chatbot.infrastructure.load_system_prompt import load_system_prompt
from src.chatbot.interface.create_app import create_app


def init_app():
    settings = load_settings()
    store = EnvApiKeyStore(".env")
    repo = JsonMemoryRepository(settings.memory_file)
    model = GeminiChatModel(settings, store)
    sys_prompt = load_system_prompt(settings.system_prompt_file)

    deps = {
        "settings": settings,
        "store": store,
        "repo": repo,
        "model": model,
        "system_prompt": sys_prompt,
    }
    return create_app(deps), settings


app, default_settings = init_app()


def main():
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    print(f"=== VetChatbot đang hoạt động tại: http://{default_settings.host}:{default_settings.port} ===")
    try:
        app.run(host=default_settings.host, port=default_settings.port, debug=False)
    except OSError:
        print(f"Lỗi: Cổng {default_settings.port} đang bị chiếm dụng. Vui lòng đổi PORT trong .env!")
        sys.exit(1)


if __name__ == "__main__":
    main()
