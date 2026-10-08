"""Nạp nội dung system prompt chuyên gia thú y từ tệp."""
from pathlib import Path

DEFAULT_VET_PROMPT = (
    "Bạn là VetGoods Assistant - Trợ lý chuyên gia tư vấn hàng hóa, thuốc và dinh dưỡng thú y. "
    "Nhiệm vụ: Cung cấp thông tin sản phẩm, hoạt chất, liều dùng theo cân nặng, đường dùng, "
    "thời gian ngưng thuốc và cảnh báo an toàn cho vật nuôi. "
    "Luôn nhắc nhở người nuôi tham vấn ý kiến trực tiếp của bác sĩ thú y cho các ca bệnh nghiêm trọng."
)


def load_system_prompt(file_path: str = "system-prompt.txt") -> str:
    """Đọc tệp system prompt, trả về mặc định nếu tệp vắng mặt hoặc rỗng."""
    path = Path(file_path)
    if not path.exists() or not path.is_file():
        return DEFAULT_VET_PROMPT
    try:
        content = path.read_text(encoding="utf-8").strip()
        return content if content else DEFAULT_VET_PROMPT
    except Exception:
        return DEFAULT_VET_PROMPT
