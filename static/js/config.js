/**
 * Cấu hình kết nối Backend API.
 * Local: "" (cùng domain).
 * Vercel: Tự động trỏ sang backend Render hoặc window.VET_API_BASE_URL.
 */
const isLocal = typeof window !== "undefined" && (
  window.location.hostname === "127.0.0.1" ||
  window.location.hostname === "localhost" ||
  window.location.hostname === ""
);

export const API_BASE_URL = window.VET_API_BASE_URL ||
  (isLocal ? "" : (localStorage.getItem("vet_api_base_url") || "https://chatbot-animal.onrender.com"));

