"""Cây phân cấp ngoại lệ nghiệp vụ của VetChatbot."""


class ChatbotError(Exception):
    """Lớp cha cho mọi lỗi nghiệp vụ trong hệ sinh thái VetChatbot."""
    pass


class ApiKeyMissing(ChatbotError):
    """Ném ra khi người dùng chưa cấu hình khóa API."""
    pass


class InvalidApiKey(ChatbotError):
    """Ném ra khi khóa API có định dạng không hợp lệ."""
    pass


class InvalidMessage(ChatbotError):
    """Ném ra khi nội dung câu hỏi tư vấn không hợp lệ."""
    pass


class InvalidSession(ChatbotError):
    """Ném ra khi mã phiên hội thoại không hợp lệ."""
    pass


class UpstreamError(ChatbotError):
    """Ném ra khi dịch vụ mô hình AI gặp sự cố."""
    def __init__(self, status: int, message: str) -> None:
        super().__init__(message)
        self.status = status
        self.message = message
