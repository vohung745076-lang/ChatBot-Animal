# PROMPT P3: Tầng Domain Thuần Khiết Cho VetChatbot (DDD & TDD)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P3 khi P2 đã hoàn tất và vượt qua kiểm thử.

---

# 1. Role (Vai trò):

Chuyên gia kiến trúc Domain-Driven Design (DDD) và Kỹ sư TDD phụ trách tầng nghiệp vụ cốt lõi (Domain Layer) của hệ thống VetChatbot.
Bạn xây dựng các thực thể nghiệp vụ: `Message`, hàm cắt gọt lịch sử hội thoại `trim_history`, cây mã lỗi nghiệp vụ `errors.py` và ba cổng giao tiếp trừu tượng (Ports): `MemoryRepository`, `ChatModel`, `ApiKeyStore`.
Bạn là "Người gác cổng thuần khiết": Tầng Domain tuyệt đối không phụ thuộc vào bất kỳ framework hay thư viện bên ngoài nào (không Flask, không LangChain, không Google Gemini, không dotenv, không đọc file trực tiếp).

---

# 2. Context (5W1H):

* **What (Là gì):** Prompt P3 xây dựng 6 file nghiệp vụ thuần túy:
  - `src/chatbot/domain/message.py`
  - `src/chatbot/domain/trim_history.py`
  - `src/chatbot/domain/errors.py`
  - `src/chatbot/domain/ports/memory_repository.py`
  - `src/chatbot/domain/ports/chat_model.py`
  - `src/chatbot/domain/ports/api_key_store.py`
  Kèm 2 file kiểm thử: `tests/test_trim_history.py` và `tests/test_domain_purity.py`.
* **Why (Tại sao quan trọng):** Quy tắc nghiệp vụ về tin nhắn, cắt gọt ngữ cảnh và các hợp đồng giao tiếp (Ports) cần độc lập hoàn toàn với công nghệ bên ngoài. Khi thay đổi thư viện LLM hoặc cơ sở dữ liệu, toàn bộ tầng Domain không bao giờ bị xáo trộn.
* **Who/Where:** Thư mục gốc `chatbot/`, Windows 11, PowerShell, thực thi qua lệnh `py`.
* **When:** Thực hiện sau P2 và trước P4 (Application).
* **How:** Thực hiện chu trình TDD: Tạo test trước (đỏ), viết mã tối thiểu trong domain (xanh), kiểm tra độ thuần khiết qua `test_domain_purity.py`.
* **Ràng buộc (Constraints):** Mỗi file một hàm hoặc một lớp; mỗi file dưới 100 dòng; cấm mọi lệnh import vào Flask, LangChain, Google Gemini, dotenv trong thư mục `src/chatbot/domain/`.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE:
- PRE.1: `src/chatbot/domain/` và `src/chatbot/domain/ports/` đã tồn tại từ P1.
- PRE.2: Kiểm thử cấu hình P2 `tests/test_load_settings.py` đã vượt qua 100%.

### POST:
- POST.1: 6 file trong domain và 2 file test được tạo ra đầy đủ.
- POST.2: `py -m pytest -q tests/test_trim_history.py` và `tests/test_domain_purity.py` đạt 100% xanh.
- POST.3: Tất cả các file đều dưới 100 dòng.

### INV:
- INV.1: `Message` chỉ chấp nhận role là `"human"` hoặc `"ai"`. Content không được để trống.
- INV.2: `trim_history` giữ nguyên thứ tự thời gian của các tin nhắn gần nhất và không làm biến đổi danh sách đầu vào.
- INV.3: Cấm tuyệt đối import công nghệ bên ngoài vào domain.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `src/chatbot/domain/message.py`
```python
"""Thực thể tin nhắn bất biến trong hệ thống VetChatbot."""
from dataclasses import dataclass


@dataclass(frozen=True)
class Message:
    """Đại diện cho một lượt phát biểu trong hội thoại tư vấn thú y."""
    role: str
    content: str

    def __post_init__(self) -> None:
        if self.role not in {"human", "ai"}:
            raise ValueError("Role chỉ được là 'human' hoặc 'ai'")
        if not isinstance(self.content, str) or not self.content.strip():
            raise ValueError("Nội dung tin nhắn không được để trống")
```

### 2. `src/chatbot/domain/trim_history.py`
```python
"""Thuật toán cắt gọt lịch sử hội thoại tư vấn thú y."""
from src.chatbot.domain.message import Message


def trim_history(messages: list[Message], limit: int) -> list[Message]:
    """Trả về tối đa `limit` tin nhắn gần nhất mà không làm thay đổi thứ tự."""
    if limit <= 0:
        raise ValueError("Limit phải lớn hơn 0")
    if not messages:
        return []
    return list(messages[-limit:])
```

### 3. `src/chatbot/domain/errors.py`
```python
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
```

### 4. `src/chatbot/domain/ports/memory_repository.py`
```python
"""Port lưu trữ lịch sử hội thoại."""
from abc import ABC, abstractmethod
from src.chatbot.domain.message import Message


class MemoryRepository(ABC):
    """Giao diện trừu tượng cho kho lưu trữ bộ nhớ phiên."""

    @abstractmethod
    def get(self, session_id: str) -> list[Message]:
        """Lấy danh sách tin nhắn theo session_id."""
        pass

    @abstractmethod
    def append(self, session_id: str, messages: list[Message]) -> None:
        """Ghi nối tiếp danh sách tin nhắn vào session."""
        pass

    @abstractmethod
    def reset(self, session_id: str) -> None:
        """Xóa toàn bộ lịch sử của session."""
        pass
```

### 5. `src/chatbot/domain/ports/chat_model.py`
```python
"""Port mô hình ngôn ngữ tương tác."""
from abc import ABC, abstractmethod
from src.chatbot.domain.message import Message


class ChatModel(ABC):
    """Giao diện trừu tượng gọi mô hình AI sinh câu trả lời tư vấn."""

    @abstractmethod
    def reply(
        self,
        system_prompt: str,
        history: list[Message],
        user_text: str
    ) -> str:
        """Sinh phản hồi tư vấn hàng hóa thú y từ mô hình AI."""
        pass
```

### 6. `src/chatbot/domain/ports/api_key_store.py`
```python
"""Port quản lý và lưu trữ API Key."""
from abc import ABC, abstractmethod


class ApiKeyStore(ABC):
    """Giao diện trừu tượng cho nơi lưu trữ khóa bí mật API."""

    @abstractmethod
    def is_configured(self) -> bool:
        """Kiểm tra xem khóa đã được cấu hình hay chưa."""
        pass

    @abstractmethod
    def get(self) -> str:
        """Lấy giá trị khóa API hiện hành."""
        pass

    @abstractmethod
    def save(self, api_key: str) -> None:
        """Lưu khóa API mới một cách an toàn."""
        pass
```

### 7. `tests/test_trim_history.py`
```python
"""Kiểm thử thuật toán cắt gọt lịch sử hội thoại."""
import pytest
from src.chatbot.domain.message import Message
from src.chatbot.domain.trim_history import trim_history


def test_trim_history_empty():
    assert trim_history([], 5) == []


def test_trim_history_fewer_than_limit():
    msgs = [Message("human", "Hỏi liều Amoxicillin"), Message("ai", "10mg/kg")]
    assert trim_history(msgs, 5) == msgs


def test_trim_history_exceeding_limit():
    msgs = [Message("human", f"Câu hỏi {i}") for i in range(10)]
    trimmed = trim_history(msgs, 3)
    assert len(trimmed) == 3
    assert trimmed[0].content == "Câu hỏi 7"
    assert trimmed[2].content == "Câu hỏi 9"


def test_trim_history_invalid_limit():
    with pytest.raises(ValueError):
        trim_history([], 0)
```

### 8. `tests/test_domain_purity.py`
```python
"""Kiểm tra độ thuần khiết của tầng Domain."""
from pathlib import Path


FORBIDDEN = {
    "flask", "langchain", "google", "genai", "dotenv",
    "os", "sys", "json", "requests", "urllib"
}


def test_domain_has_no_impure_dependencies():
    domain_dir = Path("src/chatbot/domain")
    py_files = list(domain_dir.rglob("*.py"))
    assert len(py_files) >= 6

    for file_path in py_files:
        content = file_path.read_text(encoding="utf-8")
        for line in content.splitlines():
            line_clean = line.strip()
            if line_clean.startswith("import ") or line_clean.startswith("from "):
                for pkg in FORBIDDEN:
                    err = f"Domain vi pham quy tac thuan khiet tai {file_path.name}: {line_clean}"
                    assert f" {pkg}" not in line_clean and f".{pkg}" not in line_clean, err
```
