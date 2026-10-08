"""Kiểm thử luồng nhập API key lần đầu."""
import pytest
from src.chatbot.config.settings import Settings
from src.chatbot.interface.create_app import create_app
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository


@pytest.fixture
def clean_client():
    deps = {
        "settings": Settings(),
        "store": FakeApiKeyStore(""),  # Ban đầu chưa có key
        "repo": FakeMemoryRepository(),
        "model": FakeChatModel("Tư vấn thuốc"),
        "system_prompt": "Prompt",
    }
    app = create_app(deps)
    app.config["TESTING"] = True
    return app.test_client()


def test_first_run_flow(clean_client):
    # 1. Trạng thái ban đầu: configured = False
    res_status = clean_client.get("/api/setup/status")
    assert res_status.status_code == 200
    assert res_status.get_json()["configured"] is False

    # 2. Gửi tin nhắn khi chưa có key -> mã 409
    res_chat_fail = clean_client.post("/api/chat", json={
        "session_id": "vet-session-001",
        "message": "Xin chào"
    })
    assert res_chat_fail.status_code == 409

    # 3. Người dùng nhập key -> setup thành công
    res_setup = clean_client.post("/api/setup", json={
        "api_key": "AIzaSyDummyValidGeminiApiKey12345"
    })
    assert res_setup.status_code == 200
    assert res_setup.get_json()["ok"] is True

    # 4. Kiểm tra lại trạng thái -> configured = True
    res_status2 = clean_client.get("/api/setup/status")
    assert res_status2.status_code == 200
    assert res_status2.get_json()["configured"] is True

    # 5. Gửi tin nhắn chat thành công ngay lập tức
    res_chat_ok = clean_client.post("/api/chat", json={
        "session_id": "vet-session-001",
        "message": "Hỏi liều kháng sinh"
    })
    assert res_chat_ok.status_code == 200
    assert res_chat_ok.get_json()["reply"] == "Tư vấn thuốc"
