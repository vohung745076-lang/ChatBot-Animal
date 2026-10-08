# PROMPT P0: File AGENTS.md, Quy tắc Kỹ thuật Dự án VetChatbot (Tư vấn Hàng hóa Thú y)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent) theo thứ tự từ P0 đến P9. Chỉ dán P0 vào thư mục gốc dự án `chatbot/`.

---

# 1. Role (Vai trò):

Bạn là Kỹ sư phần mềm cao cấp và Giảng viên hướng dẫn xây dựng hệ thống Web Chatbot chuyên ngành Thú y, chuyên viết đặc tả kỹ thuật chuẩn hình thức (Formal Specification) bằng tiếng Việt.

Vai trò của bạn trong prompt này: Tác giả duy nhất của file `AGENTS.md` đặt tại thư mục gốc `chatbot/`.
Bạn là người thiết lập luật chơi và chuẩn mực kỹ thuật cho AI agent lập trình trên Windows 11 bằng PowerShell và lệnh `py`.
File `AGENTS.md` là "bản hợp đồng kỹ thuật" tối cao mà AI agent bắt buộc phải đọc và tuân thủ tuyệt đối trước khi thực hiện bất kỳ lệnh sửa/tạo mã nguồn nào trong 9 prompt tiếp theo.

**Chủ đề dự án:**
Hệ thống **VetChatbot (VetGoods Assistant)** - Chatbot tư vấn, trò chuyện và cung cấp thông tin hàng hóa thú y (thuốc thú y, vắc-xin, chế phẩm sinh học, dinh dưỡng bổ sung, dụng cụ - thiết bị y tế thú y). Hệ thống tích hợp mô hình **Google Gemini** thông qua `langchain-google-genai` và được thiết kế chuẩn mực để **công khai mã nguồn an toàn lên Git (Public Repository)** mà không bao giờ để lộ API Key hay dữ liệu nhạy cảm.

Sản phẩm bàn giao của P0: Đúng một file `AGENTS.md` tại thư mục gốc, dưới 100 dòng, chứa đúng 7 điều luật kỹ thuật dán nhãn từ `## LUAT-1` đến `## LUAT-7`, kèm thứ tự đọc P0 - P9, cây thư mục được phép tạo theo Blueprint B2, quy trình nạp Gemini API Key lần đầu, và nguyên tắc ứng xử an toàn mã nguồn mở trên Git.

---

# 2. Context (5W1H):

* **What (Là gì):** P0 là prompt khởi đầu trong chuỗi 10 prompt của bản thiết kế VetChatbot, tạo ra file `AGENTS.md`. File này định nghĩa 7 điều luật cốt lõi: KISS, DDD/Clean Architecture, TDD, Quy tắc 1 hàm/file dưới 100 dòng, Quản lý cấu hình & Gemini API Key qua `.env` (bảo vệ an toàn cho Git công khai), An toàn thông tin y tế/thú y & bảo mật web (no innerHTML, localhost only), Vận hành trên Windows 11 với PowerShell bằng lệnh `py`.
* **Why (Tại sao quan trọng):** 
  1. AI lập trình cần bộ quy tắc bất biến để không tự ý sinh file bừa bãi, không vi phạm kiến trúc phân tầng, và không làm phình to file vượt quá giới hạn đọc hiểu.
  2. Dự án được công khai trên Git: Nếu AI hỏi API Key trong cửa sổ lệnh hoặc ghi cứng key vào code/test, API Key sẽ bị lộ lên Git commit history ngay lập tức. `AGENTS.md` là chốt chặn bảo mật số 1.
  3. Lĩnh vực hàng hóa thú y yêu cầu độ chuẩn xác cao về liều lượng, hoạt chất, thời gian ngưng thuốc (withdrawal period) và khuyến cáo an toàn y tế.
* **Who/Where (Ai và Ở đâu):** Độc giả trực tiếp là AI agent; người kiểm thử và nghiệm thu là kỹ sư/học viên trên Windows 11 tại thư mục `chatbot/`, ngang hàng với `run.py`, `requirements.txt`, `pytest.ini`, `.env.example`, `.gitignore`.
* **When (Khi nào):** Đọc và tạo `AGENTS.md` đầu tiên, trước khi tạo cây thư mục và môi trường ảo ở P1.
* **How (Làm như thế nào):** Kiểm tra điều kiện tiên quyết (PRE), kiểm tra tệp mục tiêu, sinh nội dung chuẩn 7 luật và các mục bắt buộc, kiểm tra hậu điều kiện (POST), đo lường bằng chứng và sẵn sàng chuyển giao cho P1.
* **Ràng buộc (Constraints):** Dưới 100 dòng; đúng 7 luật; sử dụng khóa môi trường `GEMINI_API_KEY`; tuyệt đối không dùng bash/curl/python3; luôn dùng `py`; không chạy server chặn cửa sổ dòng lệnh; không dùng `innerHTML`; chỉ lắng nghe trên `127.0.0.1` hoặc `localhost`.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE (Tiền điều kiện):
- PRE.1: Thư mục làm việc hiện tại phải là thư mục gốc của dự án `chatbot/`.
- PRE.2: Kiểm tra sự tồn tại của `.\AGENTS.md` (`Test-Path .\AGENTS.md`). Nếu đã có nội dung, hỏi xác nhận ghi đè.
- PRE.3: Kiểm tra Python Launcher `py --version` hoạt động bình thường trên Windows 11.
- PRE.4: Blueprint v4.1 Vet-Gemini được nạp đầy đủ trong ngữ cảnh (B1 đến B13).
- PRE.5: Cam kết an toàn Git: Không có bất kỳ chuỗi API key thật nào được đưa vào prompt hoặc mã nguồn.

### POST (Hậu điều kiện):
- POST.1: `AGENTS.md` tồn tại tại thư mục gốc và có độ dài dòng `< 100`.
- POST.2: Dòng đầu tiên là tiêu đề `# BLUEPRINT v4.1 AGENTS - VETCHATBOT (GEMINI API)`.
- POST.3: Chứa đúng 7 mục luật từ `## LUAT-1` đến `## LUAT-7`.
- POST.4: Chứa danh sách thứ tự đọc 10 prompt từ `P0-` đến `P9-`.
- POST.5: Chứa danh sách các tệp được phép tạo khớp chính xác với cây thư mục B2.
- POST.6: Chứa mục quy trình nhập Gemini API Key lần đầu qua giao diện Web (`/api/setup/status`, `/api/setup`).
- POST.7: Không chứa chuỗi khóa nhạy cảm (`AIzaSy...`), không chứa `innerHTML`, không cấu hình `0.0.0.0`.

### INV (Bất biến):
- INV.1: Mỗi luật có tên tiếng Anh ngắn gọn và đúng một dòng giải thích tiếng Việt có dấu.
- INV.2: Kiến trúc Clean Architecture / DDD: interface → application → domain; infrastructure → domain (ports). Domain thuần túy, không import Flask, LangChain, Google Gemini, dotenv hay hệ điều hành.
- INV.3: An toàn Git công khai: Mọi bí mật chỉ lưu trong `.env` cục bộ. File `.gitignore` luôn loại trừ `.env`, `memory.json`, `.venv`.
- INV.4: Mô hình LLM mặc định là Google Gemini (`gemini-1.5-flash`), thư viện `langchain-google-genai`.

---

## 3.BLUEPRINT. Blueprint v4.1 Vet-Gemini (Dùng chung cho toàn bộ 10 Prompt)

# BLUEPRINT v4.1: VETCHATBOT - HỆ THỐNG TƯ VẤN HÀNG HÓA THÚ Y DÙNG GEMINI API

### B1. Mục tiêu và Luồng khởi chạy lần đầu (First-Run Flow)
1. Khởi chạy: Người dùng gõ `py run.py`, server khởi động tại `http://127.0.0.1:2610` ngay cả khi CHƯA CÓ GEMINI API KEY (không được crash).
2. Trình duyệt mở trang chủ, `main.js` gọi `GET /api/setup/status`.
3. Nếu trả về `{"configured": false}` ⇒ hiển thị Modal MUI "Nhập khóa Google Gemini API" (ô password + nút Lưu).
4. Người dùng dán API key (`AIzaSy...`), bấm Lưu ⇒ gửi `POST /api/setup` với `{"api_key": "<key>"}`.
5. Server kiểm tra định dạng key hợp lệ, ghi nguyên tử (atomic write) vào `.env` (`GEMINI_API_KEY=<key>`), cập nhật bộ nhớ tiến trình, trả về `{"ok": true}`. Tuyệt đối không bao giờ trả lại key trong response.
6. Hộp thoại đóng lại, khung chat tư vấn hàng hóa thú y mở ra và sẵn sàng trò chuyện ngay mà không cần khởi động lại server.
7. An toàn Git: Mã nguồn đẩy lên GitHub chỉ chứa `.env.example`, khóa thật nằm an toàn trong `.env` cục bộ.

### B2. Cây thư mục chuẩn (Target Directory Tree)
```
chatbot/
  AGENTS.md  .env  .env.example  .gitignore  requirements.txt  pytest.ini  run.py  system-prompt.txt  memory.json  README.md
  src/chatbot/
    __init__.py
    config/          settings.py  load_settings.py  settings_error.py
    domain/          message.py  trim_history.py  errors.py  ports/memory_repository.py  ports/chat_model.py  ports/api_key_store.py
    application/     send_message.py  reset_conversation.py  configure_api_key.py  get_setup_status.py  validate_session_id.py  validate_message.py  validate_api_key.py
    infrastructure/  atomic_write_json.py  json_memory_repository.py  gemini_chat_model.py  load_system_prompt.py
                     env_api_key_store.py  atomic_write_text.py  map_gemini_error.py  mask_secret.py
    interface/       create_app.py  json_error.py  require_json.py  require_localhost.py
                     routes/health_route.py  routes/setup_status_route.py  routes/setup_route.py  routes/chat_route.py  routes/reset_route.py
  static/            index.html  js/session_id.js  js/api_status.js  js/api_setup.js  js/api_chat.js  js/api_reset.js
                     js/message_bubble.js  js/setup_dialog.js  js/chat_view.js  js/send_handler.js  js/main.js
  tests/             test_load_settings.py  test_trim_history.py  test_validators.py  test_send_message.py  test_reset_conversation.py test_configure_api_key.py
                     test_atomic_write.py  test_json_memory_repository.py  test_env_api_key_store.py  test_gemini_chat_model.py  test_map_gemini_error.py
                     test_load_system_prompt.py  test_routes.py  test_first_run_flow.py  test_domain_purity.py  test_static_rules.py
                     fakes/fake_memory_repository.py  fakes/fake_chat_model.py  fakes/fake_api_key_store.py
```
*Quy tắc thép:* Mỗi file đúng 1 hàm hoặc 1 class; mọi file đều dưới 100 dòng.

### B3. Cấu hình (`.env`)
- `GEMINI_API_KEY`: Chuỗi rỗng khi mới chạy; cập nhật qua `/api/setup`.
- `GEMINI_MODEL`: Mặc định `gemini-1.5-flash`.
- `GEMINI_TEMPERATURE`: Số thực từ 0.0 đến 2.0 (mặc định 0.2 cho tư vấn kỹ thuật chính xác).
- `GEMINI_TIMEOUT`: Thời gian chờ tính bằng giây (1 đến 300, mặc định 30).
- `HOST`: `127.0.0.1` (nghiêm cấm 0.0.0.0).
- `PORT`: `2610`.
- `MEMORY_FILE`: `memory.json`.
- `MAX_MESSAGES`: `6` (số lượng tin nhắn lịch sử giữ lại).
- `SYSTEM_PROMPT_FILE`: `system-prompt.txt`.

### B4. Nghiệp vụ Thú y trong Domain & Application
- Trợ lý chuyên trách tư vấn thông tin hàng hóa, thuốc thú y, vắc-xin, phụ gia thức ăn, vật tư y tế.
- Kiểm tra tính hợp lệ của câu hỏi tư vấn (`validate_message`).
- Trả lời rõ ràng: Thành phần hoạt chất, công dụng, liều dùng theo thể trọng (mg/kg), đường dùng (uống, tiêm, trộn thức ăn), thời gian ngưng thuốc (*withdrawal period*), và cảnh báo an toàn.

---

# 4. Nội dung chuẩn của file `AGENTS.md` (Dưới 100 dòng)

Dưới đây là nội dung chính thức mà P0 sẽ tạo ra cho `AGENTS.md`:

```markdown
# BLUEPRINT v4.1 AGENTS - VETCHATBOT (GEMINI API)

## LUAT-1: KISS
Keep solutions simple, clear, and focused strictly on veterinary goods consultation.
Dịch: Giữ giải pháp đơn giản, tập trung vào nghiệp vụ tư vấn thông tin hàng hóa thú y.

## LUAT-2: CLEAN-DDD
Interface -> Application -> Domain; Infrastructure -> Domain Ports. Domain is 100% pure.
Dịch: Tuân thủ Clean Architecture, tầng Domain hoàn toàn thuần khiết không phụ thuộc thư viện ngoài.

## LUAT-3: TDD
Write red unit tests before writing code; green code must pass without modifying assertions.
Dịch: Luôn viết bài kiểm thử trước, viết mã tối thiểu để vượt qua kiểm thử.

## LUAT-4: ONE-FN-UNDER-100-LINES
One function or class per file; every file must be strictly under 100 lines.
Dịch: Mỗi file chỉ chứa một hàm hoặc một lớp, độ dài mỗi file luôn dưới 100 dòng.

## LUAT-5: SAFE-CONFIG-AND-PUBLIC-GIT
Secrets in .env only; never commit keys or memory; safe for public Git repositories.
Dịch: Khóa bảo mật chỉ lưu trong .env; tuyệt đối không commit khóa, an toàn khi đẩy lên Git công khai.

## LUAT-6: VET-SAFETY-AND-WEB-SECURITY
Always provide safe veterinary disclaimers; no innerHTML; localhost 127.0.0.1 only.
Dịch: Luôn kèm khuyến cáo an toàn thú y; cấm dùng innerHTML; chỉ chạy cục bộ trên 127.0.0.1.

## LUAT-7: WINDOWS-POWERSHELL-PY
Run on Windows 11 with PowerShell; invoke Python only via the `py` launcher command.
Dịch: Vận hành trên Windows 11 bằng PowerShell, chỉ gọi Python thông qua lệnh `py`.

## THU-TU-DOC-P0-DEN-P9
P0-agents-md.md
P1-khung-du-an-windows.md
P2-config-va-env.md
P3-domain.md
P4-application.md
P5-infrastructure.md
P6-interface-flask.md
P7-giao-dien-mui.md
P8-system-prompt-va-chay-thu.md
P9-go-loi-va-nghiem-thu.md

## DUOC-PHEP-TAO-TEP
Chi duoc phep tao cac tep nam trong danh muc cay thu muc Blueprint B2.

## LUONG-KHOA-API-LAN-DAU
GET /api/setup/status -> false -> Dialog nhap GEMINI_API_KEY -> POST /api/setup -> .env -> chat ngay.

## HAN-XU-CUA-AI-AGENT
Khong bao gio hoi API key tren terminal; khong in khoa vao log; tuan thu 7 luat bat bien.
```
