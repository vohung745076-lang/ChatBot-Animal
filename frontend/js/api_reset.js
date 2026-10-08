import { API_BASE_URL } from "./config.js";

export async function apiReset(sessionId) {
  try {
    const res = await fetch(`${API_BASE_URL}/api/reset`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId }),
    });
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Lỗi kết nối khi làm mới" } };
  }
}
