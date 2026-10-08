"""Middleware bắt buộc request mang định dạng JSON hợp lệ."""
from functools import wraps
from flask import request
from src.chatbot.interface.json_error import json_error


def require_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return json_error(415, "unsupported_media_type", "Yêu cầu định dạng JSON")
        try:
            data = request.get_json(silent=True)
            if data is None or not isinstance(data, dict):
                return json_error(400, "bad_request", "Dữ liệu JSON không hợp lệ")
        except Exception:
            return json_error(400, "bad_request", "Dữ liệu JSON không hợp lệ")
        return f(*args, **kwargs)
    return decorated
