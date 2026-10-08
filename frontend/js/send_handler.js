import { apiChat } from "./api_chat.js";

export async function handleSendMessage({ sid, text, setMessages, setSending, openSetup }) {
  setSending(true);
  setMessages((prev) => [...prev, { role: "human", content: text }]);

  const res = await apiChat(sid, text);
  setSending(false);

  if (res.ok) {
    setMessages((prev) => [...prev, { role: "ai", content: res.data.reply }]);
  } else if (res.status === 409 || res.status === 401) {
    openSetup(res.data.message || "Khóa API không hợp lệ hoặc chưa cấu hình");
  } else {
    const err = res.data?.message || "Có lỗi khi kết nối máy chủ";
    setMessages((prev) => [...prev, { role: "ai", content: "⚠️ " + err }]);
  }
}
