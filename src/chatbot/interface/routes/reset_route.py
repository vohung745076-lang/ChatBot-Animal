"""Route xóa lịch sử cuộc trò chuyện hiện tại."""
from flask import Blueprint, jsonify, request
from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.domain.errors import ChatbotError
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json


def create_reset_bp(repo) -> Blueprint:
    bp = Blueprint("reset", __name__)

    @bp.route("/api/reset", methods=["POST"])
    @require_json
    def reset():
        data = request.get_json()
        sid = data.get("session_id", "")
        try:
            reset_conversation(repo, sid)
            return jsonify({"ok": True}), 200
        except ChatbotError as exc:
            return json_error(400, "invalid_session", str(exc))

    return bp
