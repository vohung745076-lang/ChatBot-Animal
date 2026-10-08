"""Chuẩn hóa cấu trúc phản hồi lỗi JSON."""
from flask import jsonify, Response


def json_error(status: int, code: str, message: str) -> tuple[Response, int]:
    """Trả về phản hồi JSON chuẩn có định dạng {'error': code, 'message': message}."""
    return jsonify({"error": code, "message": message}), status
