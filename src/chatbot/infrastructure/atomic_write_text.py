"""Ghi văn bản nguyên tử an toàn chống hỏng file."""
import os
import tempfile
from pathlib import Path


def atomic_write_text(file_path: str, content: str) -> None:
    """Ghi nội dung ra file tạm cùng thư mục rồi đổi tên nguyên tử."""
    target = Path(file_path).resolve()
    target.parent.mkdir(parents=True, exist_ok=True)
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            dir=str(target.parent),
            delete=False
        ) as f:
            temp_file = Path(f.name)
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(str(temp_file), str(target))
    except Exception:
        if temp_file and temp_file.exists():
            temp_file.unlink(missing_ok=True)
        raise
