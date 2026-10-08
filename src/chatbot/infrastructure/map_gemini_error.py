"""Chuyển đổi các lỗi từ Google Gemini API sang mã trạng thái và thông báo tiếng Việt."""


def map_gemini_error(exc: Exception) -> tuple[int, str]:
    """Ánh xạ ngoại lệ từ Google Gemini sang (HTTP status, Thông điệp tiếng Việt)."""
    text = str(exc).lower()
    if "api_key" in text or "unauthenticated" in text or "permission" in text or "401" in text:
        return 401, "Khóa Google Gemini API không chính xác, vui lòng nhập lại"
    if "resource_exhausted" in text or "quota" in text or "429" in text:
        return 503, "Hạn ngạch Google Gemini API đã hết hoặc dịch vụ quá tải, thử lại sau"
    if "deadline" in text or "timeout" in text or "504" in text:
        return 504, "Mô hình Google Gemini phản hồi quá thời gian quy định"
    if "unavailable" in text or "connection" in text or "503" in text or "502" in text:
        return 502, "Không kết nối được dịch vụ Google Gemini"
    return 500, "Có lỗi không mong đợi từ dịch vụ trí tuệ nhân tạo"
