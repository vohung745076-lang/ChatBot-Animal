# PROMPT P6: Tầng Giao Diện Web Flask REST API & File Khởi Chạy run.py Cho VetChatbot

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P6 khi P5 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Kỹ sư Backend Flask cao cấp chuyên thiết kế REST API an toàn, tuân thủ nguyên tắc Clean Architecture.
Bạn chịu trách nhiệm tạo dựng tầng Interface Flask cho VetChatbot gồm: Nhà máy ứng dụng `create_app`, các middleware kiểm soát truy cập (`require_localhost`, `require_json`), chuẩn hóa phản hồi lỗi dạng JSON không rò rỉ stack trace (`json_error`), 5 routes chức năng (`/api/health`, `/api/setup/status`, `/api/setup`, `/api/chat`, `/api/reset`), cùng tệp khởi chạy chính `run.py`.
Bạn bảo vệ ứng dụng trước các nguy cơ mạng: chỉ chấp nhận cấu hình API key từ localhost, giới hạn dung lượng request tối đa 16 KB.

---

# 2. Context (5W1H):

* **What:** Xây dựng các tệp trong `src/chatbot/interface/`:
  - `json_error.py`
  - `require_localhost.py`
  - `require_json.py`
  - `create_app.py`
  - `routes/health_route.py`
  - `routes/setup_status_route.py`
  - `routes/setup_route.py`
  - `routes/chat_route.py`
  - `routes/reset_route.py`
  - File chạy chính tại thư mục gốc: `run.py`
  Cùng bộ kiểm thử tại `tests/`: `test_routes.py` và `test_first_run_flow.py`.
* **Why:** REST API là cầu nối giữa giao diện người dùng web và logic nghiệp vụ tư vấn thú y. Việc xử lý lỗi tập trung ngăn chặn rò rỉ mã nguồn hoặc thông tin nhạy cảm của hệ thống ra ngoài.
* **Who/Where:** Thư mục gốc `chatbot/`, Windows 11, PowerShell, thực thi qua lệnh `py`.
* **When:** Thực hiện sau P5 (Infrastructure) và trước P7 (Giao diện Web MUI).
* **How:** TDD sử dụng Flask `test_client`, mô phỏng các request JSON và kiểm tra mã trạng thái HTTP.
* **Ràng buộc:** Cấm để lộ stack trace; mỗi file dưới 100 dòng; một hàm hoặc router trên mỗi file.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE:
- PRE.1: Thư viện `flask` đã được cài đặt trong môi trường ảo `.venv`.
- PRE.2: Toàn bộ tầng Application và Infrastructure đã sẵn sàng.

### POST:
- POST.1: Các file route và middleware trong `src/chatbot/interface/` được tạo đầy đủ.
- POST.2: `run.py` nằm tại thư mục gốc dự án.
- POST.3: `py -m pytest -q tests/test_routes.py tests/test_first_run_flow.py` đạt 100% xanh.
- POST.4: Tất cả các file đều dưới 100 dòng.

### INV:
- INV.1: Route `/api/setup` bắt buộc bọc bởi `require_localhost` (từ chối IP ngoài localhost với mã 403).
- INV.2: Dung lượng payload tối đa của request là 16 KB (`MAX_CONTENT_LENGTH = 16 * 1024`).
- INV.3: Tuyệt đối không trả về chuỗi API key trong bất kỳ phản hồi JSON nào.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `src/chatbot/interface/json_error.py`
```python
"""Chuẩn hóa cấu trúc phản hồi lỗi JSON."""
from flask import jsonify, Response


def json_error(status: int, code: str, message: str) -> tuple[Response, int]:
    """Trả về phản hồi JSON chuẩn có định dạng {'error': code, 'message': message}."""
    return jsonify({"error": code, "message": message}), status
```

### 2. `src/chatbot/interface/require_localhost.py`
```python
"""Middleware giới hạn chỉ cho phép truy cập từ localhost."""
from functools import wraps
from flask import request
from src.chatbot.interface.json_error import json_error


def require_localhost(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        remote = request.remote_addr or ""
        if remote not in {"127.0.0.1", "::1", "localhost"}:
            return json_error(403, "forbidden", "Chỉ cho phép truy cập từ localhost")
        return f(*args, **kwargs)
    return decorated
```

### 3. `src/chatbot/interface/require_json.py`
```python
"""Middleware bắt buộc request mang định dạng JSON hợp lệ."""
from functools import wraps
from flask import request
from src.chatbot.interface.json_error import json_error


def require_json(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not request.is_json:
            return json_error(415, "unsupported_media_type", "Yêu cầu định dạng JSON")
        try:
            data = request.get_json(silent=True)
            if data is None or not isinstance(data, dict):
                return json_error(400, "bad_request", "Dữ liệu JSON không hợp lệ")
        except Exception:
            return json_error(400, "bad_request", "Dữ liệu JSON không hợp lệ")
        return f(*args, **kwargs)
    return decorated
```

### 4. `src/chatbot/interface/routes/health_route.py`
```python
"""Route kiểm tra sức khỏe hệ thống."""
from flask import Blueprint, jsonify

health_bp = Blueprint("health", __name__)


@health_bp.route("/api/health", methods=["GET"])
def health():
    return jsonify({"ok": True}), 200
```

### 5. `src/chatbot/interface/routes/setup_status_route.py`
```python
"""Route kiểm tra trạng thái cấu hình khóa API."""
from flask import Blueprint, jsonify
from src.chatbot.application.get_setup_status import get_setup_status


def create_setup_status_bp(store) -> Blueprint:
    bp = Blueprint("setup_status", __name__)

    @bp.route("/api/setup/status", methods=["GET"])
    def status():
        res = get_setup_status(store)
        return jsonify(res), 200

    return bp
```

### 6. `src/chatbot/interface/routes/setup_route.py`
```python
"""Route lưu khóa Google Gemini API lần đầu."""
from flask import Blueprint, jsonify, request
from src.chatbot.application.configure_api_key import configure_api_key
from src.chatbot.domain.errors import InvalidApiKey
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json
from src.chatbot.interface.require_localhost import require_localhost


def create_setup_bp(store) -> Blueprint:
    bp = Blueprint("setup", __name__)

    @bp.route("/api/setup", methods=["POST"])
    @require_localhost
    @require_json
    def setup():
        data = request.get_json()
        key = data.get("api_key", "")
        try:
            configure_api_key(store, key)
            return jsonify({"ok": True}), 200
        except InvalidApiKey as exc:
            return json_error(400, "invalid_api_key", str(exc))
        except Exception:
            return json_error(500, "save_failed", "Không thể lưu khóa API")

    return bp
```

### 7. `src/chatbot/interface/routes/chat_route.py`
```python
"""Route tiếp nhận câu hỏi và trả về câu trả lời tư vấn thú y."""
import time
from flask import Blueprint, jsonify, request
from src.chatbot.application.send_message import send_message
from src.chatbot.domain.errors import ApiKeyMissing, ChatbotError, UpstreamError
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json


def create_chat_bp(repo, model, store, prompt_str, max_msg, model_name) -> Blueprint:
    bp = Blueprint("chat", __name__)

    @bp.route("/api/chat", methods=["POST"])
    @require_json
    def chat():
        data = request.get_json()
        sid = data.get("session_id", "")
        msg = data.get("message", "")
        start_t = time.perf_counter()
        try:
            reply = send_message(repo, model, store, prompt_str, max_msg, sid, msg)
            elapsed = int((time.perf_counter() - start_t) * 1000)
            return jsonify({"reply": reply, "model": model_name, "ms": elapsed}), 200
        except ApiKeyMissing:
            return json_error(409, "api_key_missing", "Chưa cấu hình API Key")
        except UpstreamError as exc:
            return json_error(exc.status, "upstream_error", exc.message)
        except ChatbotError as exc:
            return json_error(400, "bad_request", str(exc))
        except Exception:
            return json_error(500, "server_error", "Có lỗi xảy ra khi xử lý tin nhắn")

    return bp
```

### 8. `src/chatbot/interface/routes/reset_route.py`
```python
"""Route xóa lịch sử cuộc trò chuyện hiện tại."""
from flask import Blueprint, jsonify, request
from src.chatbot.application.reset_conversation import reset_conversation
from src.chatbot.domain.errors import ChatbotError
from src.chatbot.interface.json_error import json_error
from src.chatbot.interface.require_json import require_json


def create_reset_bp(repo) -> Blueprint:
    bp = Blueprint("reset", __name__)

    @bp.route("/api/reset", methods=["POST"])
    @require_json
    def reset():
        data = request.get_json()
        sid = data.get("session_id", "")
        try:
            reset_conversation(repo, sid)
            return jsonify({"ok": True}), 200
        except ChatbotError as exc:
            return json_error(400, "invalid_session", str(exc))

    return bp
```

### 9. `src/chatbot/interface/create_app.py`
```python
"""Nhà máy khởi tạo ứng dụng Flask với đầy đủ routes và cấu hình bảo mật."""
from flask import Flask, send_from_directory
from src.chatbot.interface.routes.chat_route import create_chat_bp
from src.chatbot.interface.routes.health_route import health_bp
from src.chatbot.interface.routes.reset_route import create_reset_bp
from src.chatbot.interface.routes.setup_route import create_setup_bp
from src.chatbot.interface.routes.setup_status_route import create_setup_status_bp


def create_app(deps: dict) -> Flask:
    app = Flask(__name__, static_folder="../../static", static_url_path="/static")
    app.config["MAX_CONTENT_LENGTH"] = 16 * 1024

    app.register_blueprint(health_bp)
    app.register_blueprint(create_setup_status_bp(deps["store"]))
    app.register_blueprint(create_setup_bp(deps["store"]))
    app.register_blueprint(create_chat_bp(
        deps["repo"], deps["model"], deps["store"],
        deps["system_prompt"], deps["settings"].max_messages,
        deps["settings"].gemini_model
    ))
    app.register_blueprint(create_reset_bp(deps["repo"]))

    @app.route("/")
    def index():
        return send_from_directory("../../static", "index.html")

    return app
```

### 10. `run.py`
```python
"""Điểm khởi chạy máy chủ VetChatbot trên Windows 11."""
import sys
from src.chatbot.config.load_settings import load_settings
from src.chatbot.infrastructure.env_api_key_store import EnvApiKeyStore
from src.chatbot.infrastructure.gemini_chat_model import GeminiChatModel
from src.chatbot.infrastructure.json_memory_repository import JsonMemoryRepository
from src.chatbot.infrastructure.load_system_prompt import load_system_prompt
from src.chatbot.interface.create_app import create_app


def main():
    settings = load_settings()
    store = EnvApiKeyStore(".env")
    repo = JsonMemoryRepository(settings.memory_file)
    model = GeminiChatModel(settings, store)
    sys_prompt = load_system_prompt(settings.system_prompt_file)

    deps = {
        "settings": settings,
        "store": store,
        "repo": repo,
        "model": model,
        "system_prompt": sys_prompt,
    }

    app = create_app(deps)
    print(f"=== VetChatbot đang hoạt động tại: http://{settings.host}:{settings.port} ===")
    try:
        app.run(host=settings.host, port=settings.port, debug=False)
    except OSError as exc:
        print(f"Lỗi: Cổng {settings.port} đang bị chiếm dụng. Vui lòng đổi PORT trong .env!")
        sys.exit(1)


if __name__ == "__main__":
    main()
```
