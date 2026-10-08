import { API_BASE_URL } from "./config.js";

export async function apiStatus() {
  try {
    const res = await fetch(`${API_BASE_URL}/api/setup/status`);
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Không thể kết nối máy chủ" } };
  }
}
