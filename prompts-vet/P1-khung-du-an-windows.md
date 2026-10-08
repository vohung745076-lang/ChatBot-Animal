# PROMPT P1: Khung Dự Án Windows 11, Venv, Dependencies Cho VetChatbot (Gemini API & Public Git)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P1 khi P0 đã hoàn tất và đạt chuẩn.

---

# 1. Role (Vai trò):

Kỹ sư phần mềm cao cấp và Giảng viên hướng dẫn thiết lập hạ tầng dự án Python trên Windows 11, chuyên về kiến trúc Clean Architecture/DDD, quản lý gói phụ thuộc và chuẩn hóa an toàn mã nguồn mở cho kho lưu trữ Git công khai (Public Git Repository).
Bạn thiết lập khung dự án cho **VetChatbot (VetGoods Assistant)** - hệ thống tư vấn thông tin hàng hóa, thuốc, vắc-xin và dinh dưỡng thú y tích hợp Google Gemini API.
Bạn tuân thủ nguyên tắc không dùng lệnh bash, luôn sử dụng PowerShell và bộ khởi chạy `py`, đảm bảo mọi file tạo ra đều dưới 100 dòng, tổ chức dạng 1 hàm/file.

---

# 2. Context (5W1H):

* **What (Là gì):** Prompt P1 dựng toàn bộ bộ khung thư mục rỗng và các tệp cấu hình nền tảng cho dự án VetChatbot theo đúng cây thư mục B2. Tạo môi trường ảo `.venv`, cài đặt các thư viện thiết yếu (`flask`, `langchain-core`, `langchain-google-genai`, `python-dotenv`, `pytest`), tạo file `.gitignore` an toàn bảo vệ API Key cho Git công khai, tạo `.env.example`, `pytest.ini`, và khung kiểm thử ban đầu `tests/`.
* **Why (Tại sao quan trọng):** 
  1. Nếu cấu trúc thư mục sai lệch ngay từ đầu, tất cả các prompt tiếp theo (từ P2 đến P9) sẽ bị lỗi đường dẫn import.
  2. Vì dự án sẽ đưa lên Git công khai (Public Git), file `.gitignore` phải được cấu hình tuyệt đối chặt chẽ để `.env` và `memory.json` không bao giờ bị đưa lên Git commit history.
  3. Sử dụng mô hình Google Gemini yêu cầu thư viện chính xác `langchain-google-genai` thay cho OpenAI.
* **Who/Where (Ai và Ở đâu):** Học viên/Kỹ sư làm việc trên Windows 11, mở PowerShell tại thư mục gốc `chatbot/`.
* **When (Khi nào):** Thực hiện ngay sau P0 (`AGENTS.md`) và trước P2 (`config/`).
* **How (Làm như thế nào):** Thực thi tuần tự: Tạo cây thư mục B2, tạo các file cấu hình nền tảng, tạo `.venv`, cài đặt thư viện qua pip, xác nhận bằng lệnh `py -m pytest -q` trả về mã thoát hợp lệ.
* **Ràng buộc (Constraints):** Tuyệt đối không hardcode API key thật; giá trị mẫu trong `.env.example` là `GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`; mọi tệp văn bản lưu dạng UTF-8; không chạy server ở bước này.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE (Tiền điều kiện):
- PRE.1: `PowerShell`: Phiên bản PowerShell >= 5.1 (`$PSVersionTable.PSVersion`).
- PRE.2: `py`: Lệnh `py --version` hoạt động và trỏ tới Python >= 3.10.
- PRE.3: Đường dẫn thư mục làm việc không chứa khoảng trắng, không nằm trong OneDrive.
- PRE.4: `AGENTS.md` đã tồn tại từ P0 và tuân thủ đúng 7 điều luật.
- PRE.5: Chưa có file code `.py` nào được viết trong `src/` (ngoại trừ các file `__init__.py` rỗng).
- PRE.6: Chưa có file `.env` chứa khóa thật tại bước này.

### POST (Hậu điều kiện):
- POST.1: Cây thư mục khớp 100% với Blueprint B2 (`src/chatbot/config`, `domain`, `domain/ports`, `application`, `infrastructure`, `interface`, `interface/routes`, `static/js`, `tests`, `tests/fakes`).
- POST.2: Tất cả các file `__init__.py` được tạo với nội dung rỗng (0 dòng).
- POST.3: `requirements.txt` chứa đúng các gói: `flask`, `langchain-core`, `langchain-google-genai`, `python-dotenv`, `pytest`.
- POST.4: `.gitignore` cấu hình chặt chẽ bảo vệ Git công khai, bắt buộc chứa: `.env`, `memory.json`, `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`.
- POST.5: `.env.example` chứa các biến mẫu với tiền tố Gemini (`GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE`, `GEMINI_MODEL=gemini-1.5-flash`, `HOST=127.0.0.1`, `PORT=2610`...).
- POST.6: `pytest.ini` cấu hình đúng đường dẫn `pythonpath = .` và `testpaths = tests`.
- POST.7: `README.md` được tạo mô tả dự án VetChatbot mã nguồn mở, hướng dẫn cài đặt và cam kết bảo mật.
- POST.8: Chạy `py -m pytest -q` thành công (exit code 0 hoặc 5 - no tests collected).

### INV (Bất biến):
- INV.1: Mọi file văn bản đều tuân thủ nguyên tắc dưới 100 dòng.
- INV.2: An toàn Git công khai: Tuyệt đối không sinh bất kỳ tệp chứa chuỗi `AIzaSy` hoặc khóa thật nào.
- INV.3: Không khởi động tiến trình server Flask trong prompt P1.

---

# 4. Các Tệp Cấu Hình Chi Tiết Cần Tạo

### 1. `requirements.txt`
```txt
flask
langchain-core
langchain-google-genai
python-dotenv
pytest
```

### 2. `pytest.ini`
```ini
[pytest]
pythonpath = .
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
```

### 3. `.gitignore` (Bảo mật tối đa cho Public Git Repository)
```gitignore
# Moi truong ao Python
.venv/
env/
venv/

# Du lieu tam & Cache
__pycache__/
*.py[cod]
*$py.class
.pytest_cache/

# TEP BI MAT & DU LIEU NHAY CAM (NGHIEM CAM DUA LEN GIT)
.env
memory.json
*.corrupt-*

# IDE & Editor
.vscode/
.idea/
*.swp
```

### 4. `.env.example`
```env
# GOOGLE GEMINI API CONFIGURATION
GEMINI_API_KEY=YOUR_GEMINI_API_KEY_HERE
GEMINI_MODEL=gemini-1.5-flash
GEMINI_TEMPERATURE=0.2
GEMINI_TIMEOUT=30

# NETWORK & RUNTIME
HOST=127.0.0.1
PORT=2610
MEMORY_FILE=memory.json
MAX_MESSAGES=6
SYSTEM_PROMPT_FILE=system-prompt.txt
```

### 5. `README.md`
```markdown
# VetChatbot - Trợ Lý Tư Vấn Hàng Hóa Thú Y

VetChatbot là hệ thống chatbot web thông minh hỗ trợ tra cứu thông tin hàng hóa, thuốc thú y, vắc-xin và dinh dưỡng cho vật nuôi, sử dụng Google Gemini API và kiến trúc Clean Architecture / DDD.

## Tính năng chính
- Tư vấn thông tin sản phẩm thú y: thành phần hoạt chất, công dụng, liều dùng theo cân nặng, đường dùng, thời gian ngưng thuốc.
- Tích hợp mô hình Google Gemini siêu nhanh và chính xác.
- Bảo mật an toàn: Khóa API được lưu trữ cục bộ trong file `.env`, không lộ trên kho mã nguồn.
- Giao diện thân thiện, chuẩn Material UI.

## Cài đặt trên Windows 11
1. Khởi tạo môi trường ảo: `py -m venv .venv`
2. Kích hoạt môi trường: `.\.venv\Scripts\Activate.ps1`
3. Cài đặt thư viện: `py -m pip install -r requirements.txt`
4. Chạy kiểm thử: `py -m pytest -q`
5. Khởi động server: `py run.py` và truy cập `http://127.0.0.1:2610`
```

---

# 5. Kịch Bản Thực Thi PowerShell Chuẩn (Windows 11)

```powershell
# 1. Tao cay thu muc theo Blueprint B2
New-Item -ItemType Directory -Force -Path src/chatbot/config
New-Item -ItemType Directory -Force -Path src/chatbot/domain/ports
New-Item -ItemType Directory -Force -Path src/chatbot/application
New-Item -ItemType Directory -Force -Path src/chatbot/infrastructure
New-Item -ItemType Directory -Force -Path src/chatbot/interface/routes
New-Item -ItemType Directory -Force -Path static/js
New-Item -ItemType Directory -Force -Path tests/fakes

# 2. Tao cac file __init__.py rong
New-Item -ItemType File -Force -Path src/chatbot/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/config/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/domain/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/domain/ports/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/application/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/infrastructure/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/interface/__init__.py
New-Item -ItemType File -Force -Path src/chatbot/interface/routes/__init__.py

# 3. Tao moi truong ao va cai dat thu vien
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install --upgrade pip
py -m pip install -r requirements.txt

# 4. Kiem tra pytest
py -m pytest -q
```
