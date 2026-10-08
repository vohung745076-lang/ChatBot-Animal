"""Route kiểm tra sức khỏe hệ thống."""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health():
    return jsonify({"ok": True}), 200
