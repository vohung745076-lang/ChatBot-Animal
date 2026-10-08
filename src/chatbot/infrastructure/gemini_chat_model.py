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
        url = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.settings.gemini_model}:generateContent?key={key}"
        )
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

        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": key,
        }
        if key.startswith("AQ.") or "." in key:
            headers["Authorization"] = f"Bearer {key}"

        try:
            res = requests.post(url, headers=headers, json=payload, timeout=self.settings.gemini_timeout)
            if not res.ok:
                data = res.json().get("error", {})
                msg = data.get("message", res.text)
                code = res.status_code
                raise UpstreamError(code, f"Lỗi Google Gemini ({code}): {msg}")

            data = res.json()
            candidates = data.get("candidates", [])
            if not candidates:
                raise UpstreamError(502, "Mô hình trả về chuỗi rỗng")
            parts = candidates[0].get("content", {}).get("parts", [])
            ans = "".join(p.get("text", "") for p in parts).strip()
            if not ans:
                raise UpstreamError(502, "Mô hình trả về nội dung rỗng")
            return ans
        except UpstreamError:
            raise
        except Exception as exc:
            status, msg = map_gemini_error(exc)
            raise UpstreamError(status, msg) from exc
