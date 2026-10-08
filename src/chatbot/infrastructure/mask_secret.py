"""Che mờ chuỗi bí mật bảo vệ an toàn trên màn hình và log."""


def mask_secret(value: str) -> str:
    """Chỉ hiển thị 4 ký tự cuối nếu chuỗi dài >= 12 ký tự."""
    if not value or not isinstance(value, str):
        return "****"
    val = value.strip()
    if len(val) < 12:
        return "****"
    return f"****{val[-4:]}"
