"""Nhà máy khởi tạo ứng dụng Flask với đầy đủ routes và cấu hình bảo mật."""
from pathlib import Path
from flask import Flask, send_from_directory
from flask_cors import CORS
from src.chatbot.interface.routes.chat_route import create_chat_bp
from src.chatbot.interface.routes.health_route import health_bp
from src.chatbot.interface.routes.reset_route import create_reset_bp
from src.chatbot.interface.routes.setup_route import create_setup_bp
from src.chatbot.interface.routes.setup_status_route import create_setup_status_bp


def create_app(deps: dict) -> Flask:
    static_dir = Path(__file__).resolve().parents[3] / "static"
    app = Flask(__name__, static_folder=str(static_dir), static_url_path="/static")
    CORS(app)
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
        return send_from_directory(str(static_dir), "index.html")

    return app
