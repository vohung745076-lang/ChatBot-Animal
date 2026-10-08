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
