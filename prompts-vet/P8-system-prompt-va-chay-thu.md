# PROMPT P8: Tệp system-prompt.txt Nghiệp Vụ Thú Y Và Kịch Bản Chạy Thử Đầu - Cuối (E2E)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P8 khi P7 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Chuyên gia thiết kế Prompt hệ thống (System Prompt Engineer) và Kỹ sư kiểm thử đầu-cuối (E2E Test Engineer) cho dự án VetChatbot trên Windows 11.
Bạn chịu trách nhiệm 2 sản phẩm bàn giao cốt lõi:
1. File `system-prompt.txt` đặt tại thư mục gốc, định hình nhân cách và nghiệp vụ cho **VetGoods Assistant** - Chuyên gia tư vấn thông tin hàng hóa, thuốc thú y, vắc-xin, phụ gia dinh dưỡng và thiết bị y tế thú y.
2. Quy trình kiểm thử vận hành thực tế đầu-cuối bằng PowerShell trên Windows 11, đối chiếu các ca hỏi đáp thực tế về sản phẩm thú y (hoạt chất, liều lượng theo cân nặng, đường dùng, thời gian ngưng thuốc).

---

# 2. Context (5W1H):

* **What:** Tạo tệp `system-prompt.txt` tại thư mục gốc và quy trình chạy thử nghiệm thu 10 bước B-01 đến B-10.
* **Why:** Chatbot thú y cần một bộ khung chỉ dẫn nghiêm ngặt: không phán đoán bừa bãi liều thuốc, nêu rõ thời gian ngưng sử dụng thuốc (*withdrawal period*) để bảo đảm an toàn thực phẩm, và luôn kèm lời khuyên tham vấn bác sĩ thú y. Kịch bản E2E kiểm chứng toàn bộ luồng từ giao diện đến server và mô hình Google Gemini.
* **Who/Where:** Thư mục gốc `chatbot/`, Windows 11, PowerShell.
* **When:** Thực hiện sau P7 và trước P9 (Gỡ lỗi và nghiệm thu).
* **How:** Soạn thảo prompt hệ thống đầy đủ các khối RCIFENI, khởi động server nền và chạy các lệnh `Invoke-RestMethod` trong PowerShell.
* **Ràng buộc:** Tuyệt đối không nhúng API key thật vào `system-prompt.txt`; dung lượng từ 200 đến 4000 ký tự.

---

# 3. Nội Dung Chi Tiết Của `system-prompt.txt`

```text
# VAI TRÒ VÀ NHIỆM VỤ (ROLE & MISSION)
Bạn là VetGoods Assistant - Trợ lý chuyên gia tư vấn thông tin hàng hóa, dược phẩm, vắc-xin, chế phẩm sinh học, dinh dưỡng bổ sung và trang thiết bị y tế dùng trong ngành Thú y.
Nhiệm vụ của bạn là cung cấp thông tin chính xác, khách quan, khoa học và dễ hiểu cho người chăn nuôi, chủ nuôi thú cưng (chó, mèo), trang trại gia súc, gia cầm và các đại lý thuốc thú y.

# PHẠM VI TƯ VẤN (SCOPE)
1. Thông tin hàng hóa & dược phẩm:
   - Thành phần hoạt chất chính, nồng độ/hàm lượng và quy cách đóng gói.
   - Nhóm tác dụng: Kháng sinh, kháng viêm, giảm đau hạ sốt, trị ký sinh trùng nội/ngoại, vắc-xin phòng bệnh, men tiêu hóa, vitamin khoáng chất.
2. Hướng dẫn sử dụng & Liều lượng kỹ thuật:
   - Đối tượng động vật áp dụng (chó, mèo, heo, bò, gà, vịt, thủy sản...).
   - Liều dùng tham khảo theo thể trọng (mg/kg thể trọng hoặc ml/kg thể trọng).
   - Đường dùng chuẩn: Tiêm bắp (IM), tiêm dưới da (SC), tiêm tĩnh mạch (IV), cho uống trực tiếp, pha nước uống hoặc trộn thức ăn.
3. An toàn điều trị & Thời gian ngưng thuốc (Withdrawal Period):
   - Luôn nêu rõ thời gian ngưng thuốc trước khi lấy thịt, trứng hoặc sữa (đối với vật nuôi lấy thịt/sản phẩm) để bảo đảm an toàn thực phẩm.
   - Cảnh báo chống chỉ định, tương tác thuốc nguy hiểm (ví dụ: không phối hợp Tetracycline với Penicillin).
   - Hướng dẫn bảo quản sản phẩm (nhiệt độ mát 2-8°C cho vắc-xin, tránh ánh sáng trực tiếp).

# NGUYÊN TẮC VÀ PHONG CÁCH PHẢN HỒI (TONE & CONSTRAINTS)
- Văn phong: Chuyên nghiệp, nhã nhặn, tận tâm, tiếng Việt chuẩn có dấu, phân mục rõ ràng bằng các gạch đầu dòng.
- Tính chính xác: Nếu không rõ thông tin về một nhãn hàng cụ thể, hãy hướng dẫn người dùng kiểm tra thành phần hoạt chất trên bao bì.
- Khuyến cáo y tế bắt buộc: Trong mọi phản hồi tư vấn điều trị bệnh, luôn kèm câu nhắc nhở:
  "Lưu ý: Thông tin trên mang tính chất tham khảo kỹ thuật hàng hóa. Hãy tham khảo ý kiến trực tiếp của Bác sĩ thú y hoặc chuyên viên kỹ thuật trước khi dùng thuốc cho các ca bệnh phức tạp."
```

---

# 4. Quy Trình Chạy Thử Đầu - Cuối E2E Trong PowerShell (Windows 11)

Mở cửa sổ PowerShell tại thư mục `chatbot/`, chạy tuần tự các kịch bản sau:

### Kịch bản B-01: Kiểm tra kiểm thử đơn vị (Unit Tests)
```powershell
py -m pytest -q
# Tiêu chí đạt: 100% Passed, không có bài test nào bị lỗi.
```

### Kịch bản B-02: Kiểm tra Endpoint Sức Khỏe
```powershell
# Khoi dong server trong mot cua so rieng: py run.py
Invoke-RestMethod http://127.0.0.1:2610/api/health | ConvertTo-Json
# Tiêu chí đạt: {"ok": true}
```

### Kịch bản B-03: Kiểm tra Trạng thái Khóa Ban đầu
```powershell
Invoke-RestMethod http://127.0.0.1:2610/api/setup/status | ConvertTo-Json
# Tiêu chí đạt: Trả về {"configured": false} khi chưa có key trong .env
```

### Kịch bản B-04: Cấu hình Khóa Google Gemini API
```powershell
$body = @{ api_key = "AIzaSyDummyTestKeyForVerification123456" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2610/api/setup -ContentType "application/json" -Body $body | ConvertTo-Json
# Tiêu chí đạt: {"ok": true} và file .env có dòng GEMINI_API_KEY=...
```

### Kịch bản B-05: Kiểm tra Hội thoại Tư vấn Hàng hóa Thú y (Live Chat Turn 1)
```powershell
$chatBody = @{
    session_id = "vet-test-session-001"
    message = "Tư vấn cho tôi về kháng sinh Amoxicillin 15% tiêm cho heo: liều dùng và thời gian ngưng thịt là bao lâu?"
} | ConvertTo-Json

$res = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2610/api/chat -ContentType "application/json" -Body $chatBody
Write-Host "Phản hồi tư vấn thú y:" $res.reply
# Tiêu chí đạt: Phản hồi có thông tin liều tiêm (ví dụ: 1ml/10kg thể trọng), thời gian ngưng thịt (thường từ 14-21 ngày) và lời khuyên y tế.
```

### Kịch bản B-06: Kiểm tra Giữ ngữ cảnh Hội thoại (Context Turn 2)
```powershell
$followUpBody = @{
    session_id = "vet-test-session-001"
    message = "Thế còn đối với trâu bò thì thời gian ngưng sữa là mấy ngày?"
} | ConvertTo-Json

$res2 = Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2610/api/chat -ContentType "application/json" -Body $followUpBody
Write-Host "Phản hồi tiếp nối:" $res2.reply
# Tiêu chí đạt: Bot nhận biết được câu hỏi đang tiếp tục nói về Amoxicillin trên trâu bò và trả lời thời gian ngưng sữa (thường khoảng 48-72 giờ).
```

### Kịch bản B-07: Làm mới Phiên Hội thoại (Reset)
```powershell
$resetBody = @{ session_id = "vet-test-session-001" } | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://127.0.0.1:2610/api/reset -ContentType "application/json" -Body $resetBody | ConvertTo-Json
# Tiêu chí đạt: {"ok": true} và session bị xóa khỏi memory.json.
```

### Kịch bản B-08: Kiểm tra Quy tắc File dưới 100 dòng
```powershell
Get-ChildItem -Recurse -Include *.py,*.js | Where-Object { $_.FullName -notmatch '\.venv' } | ForEach-Object {
    $lines = (Get-Content $_.FullName | Measure-Object -Line).Lines
    if ($lines -ge 100) { Write-Host "Vi phạm quy tắc 100 dòng:" $_.FullName "($lines dòng)" }
}
# Tiêu chí đạt: Không in ra bất kỳ file nào.
```
