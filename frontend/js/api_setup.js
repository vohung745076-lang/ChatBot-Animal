import { API_BASE_URL } from "./config.js";

export async function apiSetup(apiKey) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/setup`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ api_key: apiKey }),
    });
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Lỗi kết nối khi lưu khóa" } };
  }
}
