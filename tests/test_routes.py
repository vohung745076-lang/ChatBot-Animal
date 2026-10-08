"""Kiểm thử tích hợp các route Flask API."""
import pytest
from src.chatbot.config.settings import Settings
from src.chatbot.interface.create_app import create_app
from tests.fakes.fake_api_key_store import FakeApiKeyStore
from tests.fakes.fake_chat_model import FakeChatModel
from tests.fakes.fake_memory_repository import FakeMemoryRepository


@pytest.fixture
def client():
    deps = {
        "settings": Settings(),
        "store": FakeApiKeyStore("AIzaSyFakeKey1234567890"),
        "repo": FakeMemoryRepository(),
        "model": FakeChatModel("Tư vấn thuốc thành công"),
        "system_prompt": "Prompt",
    }
    app = create_app(deps)
    app.config["TESTING"] = True
    return app.test_client()


def test_health_route(client):
    res = client.get("/api/health")
    assert res.status_code == 200
    assert res.get_json() == {"ok": True}


def test_chat_route_success(client):
    res = client.post("/api/chat", json={
        "session_id": "vet-session-001",
        "message": "Hỏi liều Amoxicillin"
    })
    assert res.status_code == 200
    assert res.get_json()["reply"] == "Tư vấn thuốc thành công"


def test_reset_route(client):
    res = client.post("/api/reset", json={"session_id": "vet-session-001"})
    assert res.status_code == 200
    assert res.get_json() == {"ok": True}
