"""Ca sử dụng cốt lõi: Gửi câu hỏi và nhận câu trả lời tư vấn thú y."""
from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import ApiKeyMissing
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.domain.trim_history import trim_history


def send_message(
    repo: MemoryRepository,
    model: ChatModel,
    store: ApiKeyStore,
    system_prompt: str,
    max_messages: int,
    session_id: str,
    user_text: str
) -> str:
    """Điều phối toàn bộ luồng hội thoại tư vấn hàng hóa thú y."""
    valid_sid = validate_session_id(session_id)
    valid_msg = validate_message(user_text)

    if not store.is_configured():
        raise ApiKeyMissing("Chưa cấu hình Google Gemini API Key")

    raw_history = repo.get(valid_sid)
    history = trim_history(raw_history, max_messages)

    reply_text = model.reply(system_prompt, history, valid_msg)

    new_messages = [
        Message(role="human", content=valid_msg),
        Message(role="ai", content=reply_text),
    ]
    repo.append(valid_sid, new_messages)
    return reply_text
