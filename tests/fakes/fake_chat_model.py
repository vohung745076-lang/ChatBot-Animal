"""Fake implementation cho ChatModel phục vụ kiểm thử."""
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.chat_model import ChatModel


class FakeChatModel(ChatModel):
    def __init__(self, reply_text: str = "Liều dùng Amoxicillin là 10mg/kg") -> None:
        self.reply_text = reply_text
        self.calls: list[tuple[str, list[Message], str]] = []

    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        self.calls.append((system_prompt, history, user_text))
        return self.reply_text
