"""Route kiểm tra trạng thái cấu hình khóa API."""
from flask import Blueprint, jsonify
from src.chatbot.application.get_setup_status import get_setup_status


def create_setup_status_bp(store) -> Blueprint:
    bp = Blueprint("setup_status", __name__)

    @bp.route("/api/setup/status", methods=["GET"])
    def status():
        res = get_setup_status(store)
        return jsonify(res), 200

    return bp
