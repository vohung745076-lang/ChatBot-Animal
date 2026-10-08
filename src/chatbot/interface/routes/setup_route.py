"""Route lưu khóa Google Gemini API lần đầu."""
from flask import Blueprint, jsonify, request
from src.chatbot.application.configure_api_key import configure_api_key
from src.chatbot.domain.errors import InvalidApiKey
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_localhost import require_localhost


def create_setup_bp(store) -> Blueprint:
    bp = Blueprint("setup", __name__)

    @bp.route("/api/setup", methods=["POST"])
    @require_localhost
    @require_json
    def setup():
        data = request.get_json()
        key = data.get("api_key", "")
        try:
            configure_api_key(store, key)
            return jsonify({"ok": True}), 200
        except InvalidApiKey as exc:
            return json_error(400, "invalid_api_key", str(exc))
        except Exception:
            return json_error(500, "save_failed", "Không thể lưu khóa API")

    return bp
