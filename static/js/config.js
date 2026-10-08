/**
 * Cấu hình kết nối Backend API.
 * Khi deploy Vercel: Có thể truyền window.VET_API_BASE_URL = "https://your-backend.onrender.com"
 * Khi chạy Local: Mặc định "" (cùng domain).
 */
export const API_BASE_URL = window.VET_API_BASE_URL || "";
