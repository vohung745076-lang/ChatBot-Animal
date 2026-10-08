# PROMPT P9: Ma Trận Gỡ Lỗi, Khắc Phục Sự Cố Và Biên Bản Nghiệm Thu VetChatbot

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Đây là prompt cuối cùng trong chuỗi 10 prompt của dự án VetChatbot.

---

# 1. Role (Vai trò):

Kỹ sư Đảm bảo chất lượng phần mềm cao cấp (QA / Release Engineer) và Trọng tài nghiệm thu hệ thống VetChatbot.
Bạn kiểm tra chéo toàn bộ 12 ca lỗi biên (L-1 đến L-12), điều hành quy trình gỡ lỗi tối đa 3 vòng (3-Round Debugging Loop), và lập biên bản nghiệm thu kỹ thuật xác nhận hệ thống đạt chuẩn để đưa lên kho lưu trữ Git công khai (Public Git) và vận hành thực tế.

---

# 2. Context (5W1H):

* **What:** Ma trận lỗi L-1 đến L-12, quy trình khắc phục lỗi có hệ thống, và bảng tiêu chí nghiệm thu xanh (Green Acceptance Checklist).
* **Why:** Đảm bảo hệ thống đạt chuẩn sản phẩm hoàn thiện, không bị sập bất ngờ khi người dùng thao tác sai, an toàn tuyệt đối về bảo mật thông tin khi chia sẻ mã nguồn công khai trên Internet.
* **Who/Where:** Thư mục `chatbot/`, Windows 11, PowerShell.
* **When:** Thực hiện sau khi hoàn tất P0 đến P8.
* **How:** Rà soát tự động bằng lệnh PowerShell, kiểm thử ma trận lỗi, đo lường độ dài mã nguồn và xuất biên bản nghiệm thu.

---

# 3. Ma Trận 12 Ca Lỗi Biên (Matrix L-1 đến L-12)

| Mã lỗi | Tình huống phát sinh | Hành vi mong đợi của VetChatbot | Mã trạng thái |
| :--- | :--- | :--- | :--- |
| **L-1** | Chưa cấu hình `GEMINI_API_KEY` | Trả về lỗi, giao diện tự động bật hộp thoại nhập khóa | **409** `api_key_missing` |
| **L-2** | Khóa Google Gemini API bị sai / thu hồi | Bắt lỗi từ Google, trả về thông báo "Khóa không hợp lệ" | **401** `upstream_error` |
| **L-3** | Hết hạn ngạch (Quota Exceeded / Rate Limit) | Thông báo "Hạn ngạch Google Gemini API đã hết hoặc quá tải" | **503** `upstream_error` |
| **L-4** | Quá thời gian phản hồi (Timeout > 30s) | Ngắt kết nối an toàn, thông báo "Mô hình phản hồi quá lâu" | **504** `upstream_error` |
| **L-5** | Cổng mạng `PORT` (2610) bị ứng dụng khác chiếm | In thông báo tiếng Việt gợi ý đổi PORT trong `.env`, thoát code 1 | **Exit 1** |
| **L-6** | Tệp `memory.json` bị hỏng cấu trúc cú pháp | Tự đổi tên thành `memory.json.corrupt-<timestamp>`, tạo mới không crash | **200** (Tự hồi phục) |
| **L-7** | Gọi `/api/setup` từ mạng ngoài (không phải localhost) | Chặn truy cập với mã cấm truy cập | **403** `forbidden` |
| **L-8** | Header không phải `application/json` | Trả về lỗi định dạng phương tiện | **415** `unsupported_media_type` |
| **L-9** | Dữ liệu gửi lên vượt quá dung lượng 16 KB | Từ chối tiếp nhận payload quá lớn | **413** `request_entity_too_large` |
| **L-10**| `session_id` chứa ký tự lạ hoặc quá ngắn/dài | Trả về lỗi định dạng phiên hội thoại | **400** `bad_request` |
| **L-11**| Câu hỏi rỗng hoặc vượt 4000 ký tự | Báo lỗi nội dung câu hỏi không hợp lệ | **400** `bad_request` |
| **L-12**| Nguy cơ rò rỉ API Key lên Git công khai | Bị ngăn chặn hoàn toàn bởi `.gitignore` và cơ chế che mờ `mask_secret` | **Safe on Git** |

---

# 4. Quy Trình Gỡ Lỗi 3 Vòng (3-Round Debugging Loop)

Nếu có bài kiểm thử hoặc kịch bản chạy thử bị đỏ, AI agent thực hiện tuần tự tối đa 3 vòng khắc phục:

1. **Vòng 1 - Định vị nguyên nhân cốt lõi (Root Cause Analysis):**
   - Đọc kỹ thông báo lỗi và dòng mã gây lỗi.
   - Đối chiếu với hợp đồng kỹ thuật trong `AGENTS.md` và `Blueprint v4.1`.
2. **Vòng 2 - Sửa đổi tối thiểu (Minimal Refactoring):**
   - Chỉ chỉnh sửa đúng hàm và dòng code bị lỗi.
   - Không được viết gộp nhiều hàm vào một file làm phình to vượt 100 dòng.
   - Đảm bảo tầng Domain giữ vững tính thuần khiết.
3. **Vòng 3 - Kiểm chứng hồi quy (Regression Testing):**
   - Chạy lại toàn bộ `py -m pytest -q`.
   - Chạy lệnh quét kiểm tra quy tắc 100 dòng cho toàn dự án.
   - Nếu sau 3 vòng vẫn không xanh, dừng lại và báo cáo chi tiết cho người dùng.

---

# 5. Lệnh Nghiệm Thu Toàn Diện Trên Windows 11 (PowerShell)

Chạy khối lệnh sau để nghiệm thu toàn bộ hệ thống VetChatbot:

```powershell
Write-Host "================ BẮT ĐẦU NGHIỆM THU VETCHATBOT ================" -ForegroundColor Cyan

# 1. Kiem tra pytest
Write-Host "[1/4] Chạy toàn bộ Unit Tests..."
py -m pytest -q
if ($LASTEXITCODE -ne 0) { Write-Error "Kiểm thử thất bại!"; exit 1 }

# 2. Kiem tra quy tac 100 dong tren toan bo file
Write-Host "[2/4] Kiểm tra quy tắc dưới 100 dòng..."
$violations = Get-ChildItem -Recurse -Include *.py,*.js | Where-Object { $_.FullName -notmatch '\.venv' } | ForEach-Object {
    $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
    if ($lines -ge 100) { "$($_.FullName) ($lines dòng)" }
}
if ($violations) {
    Write-Host "Cảnh báo vi phạm 100 dòng:" -ForegroundColor Red
    $violations
    exit 1
} else {
    Write-Host "-> Đạt: 100% tệp đều dưới 100 dòng!" -ForegroundColor Green
}

# 3. Kiem tra do thuan khiet cua Domain
Write-Host "[3/4] Kiểm tra độ thuần khiết của Domain..."
py -m pytest -q tests/test_domain_purity.py
if ($LASTEXITCODE -ne 0) { Write-Error "Domain bị nhiễm phụ thuộc bên ngoài!"; exit 1 }

# 4. Kiem tra an toan Git (khong co file .env hay memory.json bi theo doi boi git)
Write-Host "[4/4] Kiểm tra cấu hình an toàn cho Public Git..."
if (Test-Path .\.gitignore) {
    $ign = Get-Content .\.gitignore
    if ($ign -contains ".env" -and $ign -contains "memory.json") {
        Write-Host "-> Đạt: .gitignore đã bảo vệ .env và memory.json an toàn!" -ForegroundColor Green
    } else {
        Write-Warning "Cảnh báo: .gitignore thiếu khai báo loại trừ file nhạy cảm!"
    }
}

Write-Host "================ NGHIỆM THU THÀNH CÔNG RỰC RỠ ================" -ForegroundColor Green
```
