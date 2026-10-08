# 🌿 VetChatbot - Trợ Lý Tư Vấn Hàng Hóa Thú Y

VetChatbot là hệ thống chatbot web thông minh hỗ trợ tra cứu thông tin hàng hóa, thuốc thú y, vắc-xin và dinh dưỡng cho vật nuôi, sử dụng Google Gemini API và kiến trúc Clean Architecture / DDD.

## Tính năng chính
- **Tư vấn hàng hóa thú y:** Cung cấp thông tin hoạt chất, quy cách, công dụng, liều dùng theo thể trọng (mg/kg), đường dùng (uống, tiêm, trộn thức ăn).
- **An toàn điều trị & Thời gian ngưng thuốc:** Cung cấp thông tin thời gian ngưng sử dụng thuốc (*withdrawal period*) trước khi khai thác thịt/trứng/sữa, cảnh báo tương tác thuốc và chống chỉ định.
- **Tích hợp Google Gemini:** Tốc độ phản hồi cực nhanh, chính xác cao với mô hình `gemini-1.5-flash`.
- **Bảo mật mã nguồn mở:** Khóa API được lưu cục bộ trong file `.env`, file `.gitignore` nghiêm ngặt bảo vệ thông tin khi đưa lên Git công khai.
- **Giao diện hiện đại:** Xây dựng bằng React 18 UMD và Material UI UMD không cần bước biên dịch phức tạp.

## Hướng dẫn cài đặt và khởi chạy trên Windows 11

### 1. Khởi tạo môi trường ảo
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### 2. Cài đặt các thư viện phụ thuộc
```powershell
py -m pip install -r requirements.txt
```

### 3. Kiểm thử đơn vị
```powershell
py -m pytest -q
```

### 4. Khởi động máy chủ
```powershell
py run.py
```
Sau khi server khởi động, truy cập trình duyệt tại: `http://127.0.0.1:2610` để nhập Google Gemini API Key và bắt đầu trò chuyện tư vấn!
