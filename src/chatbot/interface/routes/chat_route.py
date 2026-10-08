"""Route tiếp nhận câu hỏi và trả về câu trả lời tư vấn thú y."""
import time
from flask import Blueprint, jsonify, request
from src.chatbot.application.send_message import send_message
from src.chatbot.domain.errors import ApiKeyMissing, ChatbotError, UpstreamError
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json


def create_chat_bp(repo, model, store, prompt_str, max_msg, model_name) -> Blueprint:
    bp = Blueprint("chat", __name__)

    @bp.route("/api/chat", methods=["POST"])
    @require_json
    def chat():
        data = request.get_json()
        sid = data.get("session_id", "")
        msg = data.get("message", "")
        start_t = time.perf_counter()
        try:
            reply = send_message(repo, model, store, prompt_str, max_msg, sid, msg)
            elapsed = int((time.perf_counter() - start_t) * 1000)
            return jsonify({"reply": reply, "model": model_name, "ms": elapsed}), 200
        except ApiKeyMissing:
            return json_error(409, "api_key_missing", "Chưa cấu hình API Key")
        except UpstreamError as exc:
            return json_error(exc.status, "upstream_error", exc.message)
        except ChatbotError as exc:
            return json_error(400, "bad_request", str(exc))
        except Exception:
            return json_error(500, "server_error", "Có lỗi xảy ra khi xử lý tin nhắn")

    return bp
