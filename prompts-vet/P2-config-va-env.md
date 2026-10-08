# PROMPT P2: Tầng Cấu Hình và Xử Lý Biến Môi Trường Cho VetChatbot (Gemini API)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P2 khi P1 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Kỹ sư kiến trúc phần mềm và chuyên gia TDD phụ trách module cấu hình cho hệ thống VetChatbot (Tư vấn hàng hóa thú y).
Bạn thiết kế lớp cấu hình bất biến (Frozen Dataclass) `Settings`, hàm nạp cấu hình `load_settings` và lớp ngoại lệ `SettingsError`.
Bạn bảo vệ tuyệt đối tính an toàn cho kho lưu trữ Git công khai: Không bao giờ in giá trị của `GEMINI_API_KEY` ra thông báo lỗi, log hoặc màn hình console.
Bạn tuân thủ nguyên tắc: Mỗi file một hàm hoặc một lớp, mỗi file dưới 100 dòng, viết test trước khi viết mã nguồn (TDD).

---

# 2. Context (5W1H):

* **What (Là gì):** Prompt P2 xây dựng 3 file mã nguồn trong `src/chatbot/config/`: `settings_error.py`, `settings.py`, `load_settings.py` cùng tệp kiểm thử `tests/test_load_settings.py`.
* **Why (Tại sao quan trọng):** Cấu hình là xương sống điều khiển toàn bộ ứng dụng. Nếu cấu hình không được kiểm tra chặt chẽ, các lỗi như cổng mạng sai, host 0.0.0.0 (nguy cơ bảo mật) hoặc nhiệt độ model ngoài dải hợp lệ sẽ gây sập hệ thống. Việc ẩn giá trị API key trong thông báo lỗi là điều kiện tiên quyết để dự án an toàn khi đẩy lên Git công khai.
* **Who/Where:** Thư mục làm việc `chatbot/`, hệ điều hành Windows 11, PowerShell, sử dụng lệnh `py`.
* **When:** Thực hiện sau P1 và trước P3 (Domain).
* **How:** Viết bài kiểm thử `test_load_settings.py` trước (báo đỏ), sau đó hiện thực `settings_error.py`, `settings.py`, và `load_settings.py` cho đến khi kiểm thử xanh hoàn toàn.
* **Ràng buộc (Constraints):** Sử dụng các biến môi trường cấu hình Google Gemini (`GEMINI_API_KEY`, `GEMINI_MODEL`, `GEMINI_TEMPERATURE`, `GEMINI_TIMEOUT`); `HOST` bắt buộc là `127.0.0.1` hoặc `localhost` (từ chối `0.0.0.0`); file `.env` nếu vắng mặt thì sử dụng giá trị mặc định mà không gây crash server.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE (Tiền điều kiện):
- PRE.1: P1 đã hoàn thành; `src/chatbot/config/` và `tests/` đã sẵn sàng.
- PRE.2: Môi trường ảo `.venv` đã kích hoạt, thư viện `python-dotenv` và `pytest` đã cài đặt.

### POST (Hậu điều kiện):
- POST.1: 3 tệp nguồn được tạo trong `src/chatbot/config/`: `settings_error.py`, `settings.py`, `load_settings.py`.
- POST.2: `tests/test_load_settings.py` được tạo và kiểm tra đầy đủ các ca biên.
- POST.3: Chạy `py -m pytest -q tests/test_load_settings.py` đạt kết quả xanh (100% Passed).
- POST.4: Mọi tệp đều dưới 100 dòng.
- POST.5: Không có thông báo lỗi nào in giá trị thô của API Key.

### INV (Bất biến):
- INV.1: `Settings` là một frozen dataclass (bất biến sau khi khởi tạo).
- INV.2: Giá trị mặc định của `gemini_model` là `"gemini-1.5-flash"`.
- INV.3: Giá trị `host` không chấp nhận `"0.0.0.0"`.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `src/chatbot/config/settings_error.py`
```python
"""Ngoại lệ cấu hình cho VetChatbot."""


class SettingsError(Exception):
    """Ngoại lệ ném ra khi giá trị cấu hình không hợp lệ."""
    pass
```

### 2. `src/chatbot/config/settings.py`
```python
"""Lớp cấu hình bất biến cho hệ thống VetChatbot (Google Gemini)."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Settings:
    """Chứa toàn bộ thông số vận hành của VetChatbot."""
    gemini_api_key: str = ""
    gemini_model: str = "gemini-1.5-flash"
    gemini_temperature: float = 0.2
    gemini_timeout: int = 30
    host: str = "127.0.0.1"
    port: int = 2610
    memory_file: str = "memory.json"
    max_messages: int = 6
    system_prompt_file: str = "system-prompt.txt"
```

### 3. `src/chatbot/config/load_settings.py`
```python
"""Hàm nạp và kiểm tra tính hợp lệ của cấu hình từ file .env."""
import os
from pathlib import Path
from dotenv import dotenv_values
from src.chatbot.config.settings import Settings
from src.chatbot.config.settings_error import SettingsError


def load_settings(env_path: str = ".env") -> Settings:
    """Nạp cấu hình từ file .env và biến môi trường hệ thống."""
    vals = {}
    path = Path(env_path)
    if path.exists() and path.is_file():
        vals = dotenv_values(dotenv_path=env_path)

    def get_val(key: str, default: str) -> str:
        return vals.get(key) or os.environ.get(key) or default

    api_key = get_val("GEMINI_API_KEY", "").strip()
    model = get_val("GEMINI_MODEL", "gemini-1.5-flash").strip()
    if not model:
        raise SettingsError("GEMINI_MODEL không được để trống")

    raw_temp = get_val("GEMINI_TEMPERATURE", "0.2")
    try:
        temp = float(raw_temp)
        if not (0.0 <= temp <= 2.0):
            raise ValueError()
    except ValueError:
        raise SettingsError("GEMINI_TEMPERATURE phải là số thực từ 0.0 đến 2.0")

    raw_timeout = get_val("GEMINI_TIMEOUT", "30")
    try:
        timeout = int(raw_timeout)
        if not (1 <= timeout <= 300):
            raise ValueError()
    except ValueError:
        raise SettingsError("GEMINI_TIMEOUT phải là số nguyên từ 1 đến 300")

    host = get_val("HOST", "127.0.0.1").strip()
    if host == "0.0.0.0" or host not in {"127.0.0.1", "localhost"}:
        raise SettingsError("HOST chỉ chấp nhận 127.0.0.1 hoặc localhost")

    raw_port = get_val("PORT", "2610")
    try:
        port = int(raw_port)
        if not (1024 <= port <= 65535):
            raise ValueError()
    except ValueError:
        raise SettingsError("PORT phải là số nguyên từ 1024 đến 65535")

    raw_max = get_val("MAX_MESSAGES", "6")
    try:
        max_msg = int(raw_max)
        if not (1 <= max_msg <= 50):
            raise ValueError()
    except ValueError:
        raise SettingsError("MAX_MESSAGES phải là số nguyên từ 1 đến 50")

    memory_file = get_val("MEMORY_FILE", "memory.json").strip()
    prompt_file = get_val("SYSTEM_PROMPT_FILE", "system-prompt.txt").strip()

    return Settings(
        gemini_api_key=api_key,
        gemini_model=model,
        gemini_temperature=temp,
        gemini_timeout=timeout,
        host=host,
        port=port,
        memory_file=memory_file,
        max_messages=max_msg,
        system_prompt_file=prompt_file,
    )
```

### 4. `tests/test_load_settings.py`
```python
"""Kiểm thử unit test cho tầng cấu hình VetChatbot."""
import pytest
from src.chatbot.config.load_settings import load_settings
from src.chatbot.config.settings_error import SettingsError


def test_load_settings_defaults(tmp_path):
    non_existent = tmp_path / ".env.none"
    s = load_settings(str(non_existent))
    assert s.gemini_model == "gemini-1.5-flash"
    assert s.host == "127.0.0.1"
    assert s.port == 2610
    assert s.gemini_temperature == 0.2
    assert s.gemini_api_key == ""


def test_load_settings_custom(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text(
        "GEMINI_API_KEY=AIzaSyDummyTestKey1234567890\n"
        "GEMINI_MODEL=gemini-1.5-pro\n"
        "PORT=3000\n"
        "GEMINI_TEMPERATURE=0.7\n",
        encoding="utf-8"
    )
    s = load_settings(str(env_file))
    assert s.gemini_api_key == "AIzaSyDummyTestKey1234567890"
    assert s.gemini_model == "gemini-1.5-pro"
    assert s.port == 3000
    assert s.gemini_temperature == 0.7


def test_reject_host_all_interfaces(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("HOST=0.0.0.0\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="HOST chỉ chấp nhận"):
        load_settings(str(env_file))


def test_reject_invalid_port(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("PORT=99999\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="PORT phải là số nguyên"):
        load_settings(str(env_file))


def test_reject_invalid_temperature(tmp_path):
    env_file = tmp_path / ".env"
    env_file.write_text("GEMINI_TEMPERATURE=3.5\n", encoding="utf-8")
    with pytest.raises(SettingsError, match="GEMINI_TEMPERATURE"):
        load_settings(str(env_file))
```
