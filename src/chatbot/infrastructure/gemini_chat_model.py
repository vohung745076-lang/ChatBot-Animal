"""Tích hợp mô hình Google Gemini thông qua Google REST API."""
import requests
from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.infrastructure.map_gemini_error import map_gemini_error


class GeminiChatModel(ChatModel):
    """Hiện thực ChatModel gọi Google Gemini REST API, nạp lại API key ở mỗi lượt gửi."""

    def __init__(self, settings: Settings, store: ApiKeyStore) -> None:
        self.settings = settings
        self.store = store

    def reply(
        self,
        system_prompt: str,
        history: list[Message],
        user_text: str
    ) -> str:
        key = self.store.get()
        models_to_try = [self.settings.gemini_model]
        fallbacks = [
            "gemini-3.5-flash",
            "gemini-3.1-flash-lite",
            "gemini-flash-lite-latest",
            "gemini-3.8-flash"
        ]
        for fb in fallbacks:
            if fb not in models_to_try:
                models_to_try.append(fb)

        contents = []
        for h in history:
            role = "user" if h.role == "human" else "model"
            contents.append({"role": role, "parts": [{"text": h.content}]})
        contents.append({"role": "user", "parts": [{"text": user_text}]})

        payload = {
            "system_instruction": {"parts": [{"text": system_prompt}]},
            "contents": contents,
            "generationConfig": {"temperature": self.settings.gemini_temperature}
        }

        headers = {"Content-Type": "application/json", "x-goog-api-key": key}
        last_error = None

        for mdl in models_to_try:
            url = f"https://generativelanguage.googleapis.com/v1beta/models/{mdl}:generateContent?key={key}"
            try:
                res = requests.post(url, headers=headers, json=payload, timeout=self.settings.gemini_timeout)
                if not res.ok:
                    data = res.json().get("error", {})
                    msg = data.get("message", res.text)
                    if res.status_code in (404, 429, 503) and mdl != models_to_try[-1]:
                        continue
                    status, mapped = map_gemini_error(Exception(f"{res.status_code} {msg}"))
                    raise UpstreamError(status, mapped)

                data = res.json()
                cands = data.get("candidates", [])
                if not cands:
                    raise UpstreamError(502, "Mô hình trả về chuỗi rỗng")
                parts = cands[0].get("content", {}).get("parts", [])
                ans = "".join(p.get("text", "") for p in parts).strip()
                if not ans:
                    raise UpstreamError(502, "Mô hình trả về nội dung rỗng")
                return ans
            except UpstreamError:
                raise
            except requests.RequestException as req_err:
                last_error = req_err
                if mdl != models_to_try[-1]:
                    continue
            except Exception as exc:
                last_error = exc

        status, mapped_msg = map_gemini_error(last_error or Exception("Không thể kết nối"))
        raise UpstreamError(status, mapped_msg)
