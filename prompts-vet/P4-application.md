# PROMPT P4: Tầng Ứng Dụng (Application Use Cases) Cho VetChatbot

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P4 khi P3 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Kỹ sư phần mềm chuyên về tầng điều phối nghiệp vụ (Application Service / Use Cases) theo Clean Architecture.
Bạn chịu trách nhiệm xây dựng các ca sử dụng (Use Cases) của hệ thống VetChatbot: xác thực dữ liệu đầu vào (câu hỏi tư vấn, mã phiên, khóa Google Gemini API), kiểm tra trạng thái cấu hình, lưu khóa API an toàn, xóa phiên hội thoại, và use case trung tâm `send_message` phục vụ hỏi đáp thông tin hàng hóa thú y.
Bạn tuân thủ quy tắc 1 hàm / 1 file, mỗi file dưới 100 dòng, không gắn chặt với bất kỳ giao diện web nào.

---

# 2. Context (5W1H):

* **What:** Xây dựng 7 file use case và validator tại `src/chatbot/application/`:
  - `validate_session_id.py`
  - `validate_message.py`
  - `validate_api_key.py`
  - `get_setup_status.py`
  - `configure_api_key.py`
  - `reset_conversation.py`
  - `send_message.py`
  Cùng bộ kiểm thử tại `tests/`: `test_validators.py`, `test_send_message.py`, `test_reset_conversation.py`, `test_configure_api_key.py`.
* **Why:** Tầng Application là nơi kết nối giữa giao diện và nghiệp vụ cốt lõi. Kiểm soát chặt chẽ điều kiện tiên quyết (session hợp lệ, nội dung câu hỏi không độc hại, key đã cấu hình) trước khi gọi LLM giúp tiết kiệm chi phí gọi Gemini API và đảm bảo an toàn vận hành.
* **Who/Where:** Thư mục `chatbot/`, Windows 11, PowerShell, sử dụng lệnh `py`.
* **When:** Thực hiện sau P3 (Domain) và trước P5 (Infrastructure).
* **How:** Viết test với các Fake repository/model trước, sau đó hiện thực các hàm use case.
* **Ràng buộc:** Cấm phụ thuộc vào Flask hay framework web; bảo vệ key; định dạng API Key tương thích với Google Gemini.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE:
- PRE.1: Tầng Domain P3 đã hoàn tất, các ngoại lệ và Ports đã sẵn sàng.
- PRE.2: Thư mục `tests/fakes/` đã được tạo để chứa các Fake Mock phục vụ kiểm thử đơn vị.

### POST:
- POST.1: 7 file mã nguồn được tạo trong `src/chatbot/application/`.
- POST.2: 4 file test đơn vị được tạo trong `tests/` cùng các Fake object.
- POST.3: Tất cả test chạy bằng lệnh `py -m pytest -q` đạt trạng thái xanh (Passed 100%).
- POST.4: Mọi file đều dưới 100 dòng.

### INV:
- INV.1: Thứ tự thực thi trong `send_message`: Xác thực session -> Xác thực message -> Kiểm tra khóa API -> Đọc và cắt gọt bộ nhớ -> Gọi mô hình -> Ghi tin nhắn vào bộ nhớ -> Trả về kết quả.
- INV.2: Nếu gọi mô hình sinh lỗi, TUYỆT ĐỐI KHÔNG ghi tin nhắn người dùng hay lỗi vào bộ nhớ `MemoryRepository`.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `src/chatbot/application/validate_session_id.py`
```python
"""Kiểm tra tính hợp lệ của mã phiên hội thoại."""
import re
from src.chatbot.domain.errors import InvalidSession

SESSION_REGEX = re.compile(r"^[A-Za-z0-9-]{8,64}$")


def validate_session_id(session_id: str) -> str:
    """Xác thực session_id gồm từ 8 đến 64 ký tự an toàn."""
    if not isinstance(session_id, str) or not SESSION_REGEX.match(session_id.strip()):
        raise InvalidSession("Mã phiên hội thoại không hợp lệ (cần từ 8-64 ký tự hợp lệ)")
    return session_id.strip()
```

### 2. `src/chatbot/application/validate_message.py`
```python
"""Kiểm tra nội dung câu hỏi tư vấn hàng hóa thú y."""
from src.chatbot.domain.errors import InvalidMessage


def validate_message(text: str) -> str:
    """Xác thực câu hỏi tư vấn thú y không rỗng và không vượt quá 4000 ký tự."""
    if not isinstance(text, str):
        raise InvalidMessage("Nội dung câu hỏi phải là chuỗi ký tự")
    clean = text.strip()
    if not clean:
        raise InvalidMessage("Nội dung câu hỏi tư vấn không được để trống")
    if len(clean) > 4000:
        raise InvalidMessage("Nội dung câu hỏi quá dài (tối đa 4000 ký tự)")
    return clean
```

### 3. `src/chatbot/application/validate_api_key.py`
```python
"""Kiểm tra định dạng khóa Google Gemini API."""
from src.chatbot.domain.errors import InvalidApiKey


def validate_api_key(api_key: str) -> str:
    """Xác thực định dạng Google Gemini API Key an toàn."""
    if not isinstance(api_key, str):
        raise InvalidApiKey("Khóa API phải là chuỗi ký tự")
    clean = api_key.strip()
    if len(clean) < 20 or len(clean) > 100:
        raise InvalidApiKey("Độ dài khóa API không hợp lệ (từ 20 đến 100 ký tự)")
    if any(c.isspace() for c in clean):
        raise InvalidApiKey("Khóa API không được chứa khoảng trắng")
    if not clean.isascii() or not clean.isprintable():
        raise InvalidApiKey("Khóa API chỉ được chứa các ký tự ASCII in được")
    return clean
```

### 4. `src/chatbot/application/get_setup_status.py`
```python
"""Ca sử dụng lấy trạng thái cấu hình khóa API."""
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def get_setup_status(store: ApiKeyStore) -> dict:
    """Trả về trạng thái đã cấu hình khóa hay chưa."""
    return {"configured": store.is_configured()}
```

### 5. `src/chatbot/application/configure_api_key.py`
```python
"""Ca sử dụng lưu khóa API từ người dùng."""
from src.chatbot.application.validate_api_key import validate_api_key
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


def configure_api_key(store: ApiKeyStore, raw_key: str) -> None:
    """Xác thực và lưu khóa API mới."""
    valid_key = validate_api_key(raw_key)
    store.save(valid_key)
```

### 6. `src/chatbot/application/reset_conversation.py`
```python
"""Ca sử dụng làm mới cuộc trò chuyện."""
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.ports.memory_repository import MemoryRepository


def reset_conversation(repo: MemoryRepository, session_id: str) -> None:
    """Xác thực session_id và xóa lịch sử hội thoại."""
    valid_id = validate_session_id(session_id)
    repo.reset(valid_id)
```

### 7. `src/chatbot/application/send_message.py`
```python
"""Ca sử dụng cốt lõi: Gửi câu hỏi và nhận câu trả lời tư vấn thú y."""
from src.chatbot.application.validate_message import validate_message
from src.chatbot.application.validate_session_id import validate_session_id
from src.chatbot.domain.errors import ApiKeyMissing
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.api_key_store import ApiKeyStore
from src.chatbot.domain.ports.chat_model import ChatModel
from src.chatbot.domain.ports.memory_repository import MemoryRepository
from src.chatbot.domain.trim_history import trim_history


def send_message(
    repo: MemoryRepository,
    model: ChatModel,
    store: ApiKeyStore,
    system_prompt: str,
    max_messages: int,
    session_id: str,
    user_text: str
) -> str:
    """Điều phối toàn bộ luồng hội thoại tư vấn hàng hóa thú y."""
    valid_sid = validate_session_id(session_id)
    valid_msg = validate_message(user_text)

    if not store.is_configured():
        raise ApiKeyMissing("Chưa cấu hình Google Gemini API Key")

    raw_history = repo.get(valid_sid)
    history = trim_history(raw_history, max_messages)

    reply_text = model.reply(system_prompt, history, valid_msg)

    new_messages = [
        Message(role="human", content=valid_msg),
        Message(role="ai", content=reply_text),
    ]
    repo.append(valid_sid, new_messages)
    return reply_text
```

### 8. `tests/fakes/fake_api_key_store.py`
```python
"""Fake implementation cho ApiKeyStore phục vụ kiểm thử."""
from src.chatbot.domain.ports.api_key_store import ApiKeyStore


class FakeApiKeyStore(ApiKeyStore):
    def __init__(self, key: str = "") -> None:
        self._key = key

    def is_configured(self) -> bool:
        return bool(self._key)

    def get(self) -> str:
        return self._key

    def save(self, api_key: str) -> None:
        self._key = api_key
```

### 9. `tests/fakes/fake_memory_repository.py`
```python
"""Fake implementation cho MemoryRepository phục vụ kiểm thử."""
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.memory_repository import MemoryRepository


class FakeMemoryRepository(MemoryRepository):
    def __init__(self) -> None:
        self.data: dict[str, list[Message]] = {}

    def get(self, session_id: str) -> list[Message]:
        return list(self.data.get(session_id, []))

    def append(self, session_id: str, messages: list[Message]) -> None:
        if session_id not in self.data:
            self.data[session_id] = []
        self.data[session_id].extend(messages)

    def reset(self, session_id: str) -> None:
        self.data.pop(session_id, None)
```

### 10. `tests/fakes/fake_chat_model.py`
```python
"""Fake implementation cho ChatModel phục vụ kiểm thử."""
from src.chatbot.domain.message import Message
from src.chatbot.domain.ports.chat_model import ChatModel


class FakeChatModel(ChatModel):
    def __init__(self, reply_text: str = "Liều dùng Amoxicillin là 10mg/kg") -> None:
        self.reply_text = reply_text
        self.calls: list[tuple[str, list[Message], str]] = []

    def reply(self, system_prompt: str, history: list[Message], user_text: str) -> str:
        self.calls.append((system_prompt, history, user_text))
        return self.reply_text
```

### 11. `tests/test_send_message.py`
```python
"""Kiểm thử ca sử dụng gửi tin nhắn tư vấn thú y."""
import pytest
from src.chatbot.application.send_message import send_message
from src.chatbot.domain.errors import ApiKeyMissing
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository


def test_send_message_success():
    repo = FakeMemoryRepository()
    model = FakeChatModel("Thuốc Amoxicillin 15% dạng hỗn dịch tiêm")
    store = FakeApiKeyStore("AIzaSyFakeKey1234567890")
    reply = send_message(repo, model, store, "System prompt", 5, "session-12345", "Tư vấn thuốc")
    assert reply == "Thuốc Amoxicillin 15% dạng hỗn dịch tiêm"
    assert len(repo.get("session-12345")) == 2


def test_send_message_missing_key():
    repo = FakeMemoryRepository()
    model = FakeChatModel()
    store = FakeApiKeyStore("")
    with pytest.raises(ApiKeyMissing):
        send_message(repo, model, store, "Sys", 5, "session-12345", "Tư vấn")
    assert len(repo.get("session-12345")) == 0
```
