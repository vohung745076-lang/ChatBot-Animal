"""Middleware giới hạn chỉ cho phép truy cập từ localhost."""
from functools import wraps
from flask import request
from src.chatbot.interface.json_error import json_error


def require_localhost(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        remote = request.remote_addr or ""
        if remote not in {"127.0.0.1", "::1", "localhost"}:
            return json_error(403, "forbidden", "Chỉ cho phép truy cập từ localhost")
        return f(*args, **kwargs)
    return decorated
