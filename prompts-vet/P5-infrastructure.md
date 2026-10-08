# PROMPT P5: Tầng Hạ Tầng Kỹ Thuật (Infrastructure) Tích Hợp Google Gemini API

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P5 khi P4 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Kỹ sư hạ tầng cao cấp (Infrastructure Engineer) chuyên về tích hợp mô hình ngôn ngữ lớn Google Gemini (`langchain-google-genai`), kỹ thuật ghi tệp nguyên tử (Atomic File Writing), và lưu trữ dữ liệu an toàn phục vụ kho mã nguồn mở Git.
Bạn chịu trách nhiệm cài đặt các cổng kết nối (Ports) mà tầng Domain đã định nghĩa: `JsonMemoryRepository`, `EnvApiKeyStore`, và `GeminiChatModel`.
Bạn đảm bảo việc che mờ khóa bí mật (`mask_secret`) trong mọi ghi nhận log, và phân loại chính xác các mã lỗi từ máy chủ Google Gemini sang định dạng chuẩn tiếng Việt.

---

# 2. Context (5W1H):

* **What:** Xây dựng 8 file mã nguồn tại `src/chatbot/infrastructure/`:
  - `atomic_write_text.py`
  - `atomic_write_json.py`
  - `json_memory_repository.py`
  - `load_system_prompt.py`
  - `env_api_key_store.py`
  - `mask_secret.py`
  - `map_gemini_error.py`
  - `gemini_chat_model.py`
  Cùng bộ kiểm thử tại `tests/`: `test_atomic_write.py`, `test_json_memory_repository.py`, `test_env_api_key_store.py`, `test_map_gemini_error.py`, `test_load_system_prompt.py`, `test_gemini_chat_model.py`.
* **Why:** Hạ tầng là nơi tiếp xúc trực tiếp với tệp tin và mạng Internet bên ngoài. Kỹ thuật ghi nguyên tử giúp file `.env` và `memory.json` không bao giờ bị hỏng dở dang nếu mất điện hoặc crash. Bộ chuyển đổi lỗi Gemini giúp người dùng nhận thông điệp tiếng Việt thân thiện thay vì stack trace thô thiển.
* **Who/Where:** Thư mục `chatbot/`, Windows 11, PowerShell, sử dụng lệnh `py`.
* **When:** Thực hiện sau P4 (Application) và trước P6 (Interface Flask).
* **How:** TDD với các kịch bản ghi đè file, file lỗi cú pháp JSON, và nạp prompt hệ thống tư vấn thú y.
* **Ràng buộc:** Cấm để lộ khóa API; mỗi file dưới 100 dòng; một hàm hoặc một lớp trên mỗi file.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE:
- PRE.1: `langchain-google-genai` đã được cài đặt trong `.venv`.
- PRE.2: Các cổng trừu tượng trong `src/chatbot/domain/ports/` đã có sẵn từ P3.

### POST:
- POST.1: 8 file hạ tầng được tạo đầy đủ.
- POST.2: `tests/` có đầy đủ các bài test kiểm thử hạ tầng và chạy xanh 100%.
- POST.3: Tất cả các file đều dưới 100 dòng.

### INV:
- INV.1: `GeminiChatModel` đọc lại khóa API từ `store.get()` ở MỖI lượt gọi, giúp chat được ngay sau khi người dùng lưu key qua web mà không cần khởi động lại server.
- INV.2: `mask_secret` chỉ hiển thị 4 ký tự cuối nếu key dài >= 12 ký tự, còn lại thay bằng `"****"`.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `src/chatbot/infrastructure/atomic_write_text.py`
```python
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
```

### 2. `src/chatbot/infrastructure/atomic_write_json.py`
```python
"""Ghi dữ liệu JSON nguyên tử chuẩn UTF-8."""
import json
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


def atomic_write_json(file_path: str, data: dict) -> None:
    """Chuyển đổi dữ liệu sang chuỗi JSON và ghi nguyên tử."""
    serialized = json.dumps(data, ensure_ascii=False, indent=2)
    atomic_write_text(file_path, serialized)
```

### 3. `src/chatbot/infrastructure/mask_secret.py`
```python
"""Che mờ chuỗi bí mật bảo vệ an toàn trên màn hình và log."""


def mask_secret(value: str) -> str:
    """Chỉ hiển thị 4 ký tự cuối nếu chuỗi dài >= 12 ký tự."""
    if not value or not isinstance(value, str):
        return "****"
    val = value.strip()
    if len(val) < 12:
        return "****"
    return f"****{val[-4:]}"
```

### 4. `src/chatbot/infrastructure/load_system_prompt.py`
```python
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
```

### 5. `src/chatbot/infrastructure/env_api_key_store.py`
```python
"""Lưu trữ và đồng bộ Google Gemini API Key vào file .env."""
import os
from pathlib import Path
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.infrastructure.atomic_write_text import atomic_write_text


class EnvApiKeyStore(ApiKeyStore):
    """Cài đặt lưu khóa API vào file .env và cập nhật os.environ."""

    def __init__(self, env_path: str = ".env") -> None:
        self.env_path = env_path

    def is_configured(self) -> bool:
        return bool(self.get())

    def get(self) -> str:
        val = os.environ.get("GEMINI_API_KEY", "").strip()
        if val:
            return val
        path = Path(self.env_path)
        if path.exists() and path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip()
        return ""

    def save(self, api_key: str) -> None:
        clean = api_key.strip()
        lines = []
        path = Path(self.env_path)
        found = False
        if path.exists() and path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip().startswith("GEMINI_API_KEY="):
                    lines.append(f"GEMINI_API_KEY={clean}")
                    found = True
                else:
                    lines.append(line)
        if not found:
            lines.append(f"GEMINI_API_KEY={clean}")
        atomic_write_text(self.env_path, "\n".join(lines) + "\n")
        os.environ["GEMINI_API_KEY"] = clean
```

### 6. `src/chatbot/infrastructure/json_memory_repository.py`
```python
"""Kho lưu trữ lịch sử hội thoại dạng JSON an toàn với luồng (Thread-safe)."""
import json
import threading
import time
from pathlib import Path
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.infrastructure.atomic_write_json import atomic_write_json


class JsonMemoryRepository(MemoryRepository):
    """Quản lý các phiên hội thoại trong file memory.json."""

    def __init__(self, file_path: str = "memory.json") -> None:
        self.file_path = file_path
        self._lock = threading.Lock()

    def _read_all(self) -> dict:
        path = Path(self.file_path)
        if not path.exists() or not path.is_file():
            return {}
        try:
            content = path.read_text(encoding="utf-8").strip()
            return json.loads(content) if content else {}
        except Exception:
            corrupt = path.parent / f"memory.json.corrupt-{int(time.time())}"
            path.rename(corrupt)
            return {}

    def get(self, session_id: str) -> list[Message]:
        with self._lock:
            data = self._read_all()
            raw_msgs = data.get(session_id, [])
            return [Message(m["role"], m["content"]) for m in raw_msgs]

    def append(self, session_id: str, messages: list[Message]) -> None:
        with self._lock:
            data = self._read_all()
            if session_id not in data:
                data[session_id] = []
            for m in messages:
                data[session_id].append({"role": m.role, "content": m.content})
            atomic_write_json(self.file_path, data)

    def reset(self, session_id: str) -> None:
        with self._lock:
            data = self._read_all()
            if session_id in data:
                data.pop(session_id, None)
                atomic_write_json(self.file_path, data)
```

### 7. `src/chatbot/infrastructure/map_gemini_error.py`
```python
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
```

### 8. `src/chatbot/infrastructure/gemini_chat_model.py`
```python
"""Tích hợp mô hình Google Gemini thông qua langchain-google-genai."""
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from src.chatbot.config.settings import Settings
from src.chatbot.domain.errors import UpstreamError
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.infrastructure.map_gemini_error import map_gemini_error


class GeminiChatModel(ChatModel):
    """Hiện thực ChatModel gọi Google Gemini, nạp lại API key ở mỗi lượt gửi."""

    def __init__(self, settings: Settings, store: ApiKeyStore) -> None:
        self.settings = settings
        self.store = store

    def reply(
        self,
        system_prompt: str,
        history: list[Message],
        user_text: str
    ) -> str:
        key = self.store.get()
        llm = ChatGoogleGenerativeAI(
            model=self.settings.gemini_model,
            temperature=self.settings.gemini_temperature,
            timeout=self.settings.gemini_timeout,
            google_api_key=key,
        )
        msgs = [SystemMessage(content=system_prompt)]
        for h in history:
            if h.role == "human":
                msgs.append(HumanMessage(content=h.content))
            else:
                msgs.append(AIMessage(content=h.content))
        msgs.append(HumanMessage(content=user_text))

        try:
            res = llm.invoke(msgs)
            ans = str(res.content).strip()
            if not ans:
                raise UpstreamError(502, "Mô hình trả lời chuỗi rỗng")
            return ans
        except UpstreamError:
            raise
        except Exception as exc:
            status, msg = map_gemini_error(exc)
            raise UpstreamError(status, msg) from exc
```
