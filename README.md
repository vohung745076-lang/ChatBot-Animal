# 🌿 VetChatbot - Trợ Lý Tư Vấn Sản Phẩm & Dược Thú Y Thực Tế

VetChatbot là hệ thống chatbot web thông minh chuyên dụng cho cơ sở thú y, phòng khám và đại lý thuốc thú y, tích hợp Google Gemini API (`gemini-1.5-flash`), hỗ trợ đầy đủ các định dạng khóa API (bao gồm tiền tố `AQ.` và `AIzaSy.`), kiến trúc Clean Architecture / DDD, sẵn sàng triển khai miễn phí trên **Render (Backend)** và **Vercel (Frontend)**.

---

## 🎯 Tính Năng & Nghiệp Vụ Thực Tế 100% Cho Cơ Sở Thú Y
1. **Dược phẩm & Biệt dược thông dụng tại Việt Nam:**
   - Kháng sinh đặc trị: Amoxicillin 15% LA, Enrofloxacin 10%, Florfenicol 30%, Doxycycline, Tylosin, Oxytetracycline...
   - Trị ký sinh trùng & ve rận: Ivermectin 1%, Fipronil nhỏ gáy (Fronil Spot), Praziquantel sổ giun...
   - Vắc-xin phòng bệnh: DHPPI-L (chó mèo), Dịch tả lợn, Newcastle, Gumboro (gia cầm)...
   - Trợ sức & Hạ sốt: Catosal, B-Complex, Ketoprofen, Analgin-C, Gluco-K-C thảo dược...
2. **Nghiệp vụ tư vấn bán hàng chuyên nghiệp:**
   - Cung cấp quy cách đóng gói (20ml, 100ml, 100g, 1kg) và mức giá tham khảo thị trường.
   - Gợi ý Combo điều trị (Cross-selling): Kháng sinh kèm Trợ sức/Men tiêu hóa; Diệt ve kèm Xịt khử trùng chuồng; Vắc-xin kèm Tẩy giun.
   - Tự động tính toán lượng thuốc cần mua theo số lượng con và cân nặng của đàn.
3. **An toàn điều trị & Thời gian ngưng thuốc (Withdrawal Period):**
   - Nêu rõ số ngày ngưng thuốc trước khi khai thác thịt, trứng, sữa.
   - Cảnh báo chống chỉ định và tương tác thuốc nguy hiểm.

---

## 🚀 Hướng Dẫn Deploy Miễn Phí Lên Cloud

### 1. Đẩy mã nguồn lên GitHub cá nhân
Mở PowerShell tại thư mục dự án:
```powershell
# Tạo repo mới trên GitHub (ví dụ: https://github.com/<username>/vetchatbot.git)
git remote add origin https://github.com/<username>/vetchatbot.git
git branch -M main
git push -u origin main
```

### 2. Deploy Backend lên Render (Miễn phí)
1. Đăng nhập [render.com](https://render.com) và liên kết với tài khoản GitHub.
2. Chọn **New +** ➔ **Web Service** ➔ Chọn repo `vetchatbot`.
3. Cấu hình:
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `gunicorn run:app --bind 0.0.0.0:$PORT`
   - **Environment Variables:**
     - `GEMINI_API_KEY`: Dán khóa Google Gemini API của bạn (bắt đầu bằng `AQ.` hoặc `AIzaSy.`)
     - `GEMINI_MODEL`: `gemini-1.5-flash`
     - `HOST`: `0.0.0.0`
4. Bấm **Deploy Web Service**. Sau vài phút, Render sẽ cung cấp URL Backend của bạn (ví dụ: `https://vetchatbot-backend.onrender.com`).

### 3. Deploy Frontend lên Vercel (Miễn phí)
1. Đăng nhập [vercel.com](https://vercel.com) và chọn **Add New...** ➔ **Project**.
2. Chọn repo `vetchatbot` từ GitHub.
3. Trong phần **Root Directory**, chọn `frontend` (hoặc để mặc định root với file `vercel.json` đã có sẵn).
4. Bấm **Deploy**.
5. Trong `frontend/js/config.js`, điền URL Backend trên Render vừa tạo:
   ```javascript
   export const API_BASE_URL = "https://vetchatbot-backend.onrender.com";
   ```
6. Frontend trên Vercel và Backend trên Render sẽ tự động kết nối qua CORS và vận hành 24/7 hoàn toàn miễn phí!

---

## 💻 Chạy Cục Bộ Trên Windows 11
```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
py -m pip install -r requirements.txt
py -m pytest -q
py run.py
```
Truy cập tại: `http://127.0.0.1:2610`
