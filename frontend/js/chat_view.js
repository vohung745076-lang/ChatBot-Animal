const e = React.createElement;
const { Box, AppBar, Toolbar, Typography, TextField, Button, Chip } = MaterialUI;
import { MessageBubble } from "./message_bubble.js";

const SUGGESTIONS = [
  "Giá & liều Amoxicillin 15% LA",
  "Liều Enrofloxacin cho heo 40kg",
  "Thuốc trị ve rận & ghẻ chó mèo",
  "Tính lượng thuốc đàn 20 con heo"
];

export function ChatView({ messages, onSend, onReset, sending }) {
  const [text, setText] = React.useState("");
  const endRef = React.useRef(null);

  React.useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = (msgText) => {
    const toSend = (msgText || text).trim();
    if (!toSend || sending) return;
    onSend(toSend);
    setText("");
  };

  return e(
    Box,
    { sx: { width: "100%", maxWidth: 880, height: "100vh", display: "flex", flexDirection: "column" } },
    e(AppBar, { position: "static", sx: { bgcolor: "#2e7d32" } },
      e(Toolbar, null,
        e(Typography, { variant: "h6", sx: { flexGrow: 1, display: "flex", alignItems: "center", gap: 1 } },
          "🌿 VetChatbot - Tư Vấn Hàng Hóa Thú Y",
          e("span", { style: { fontSize: "0.75rem", color: "#b9f6ca" } }, "● Online")
        ),
        e(Button, { color: "inherit", onClick: onReset }, "Làm mới")
      )
    ),
    e(Box, { sx: { flexGrow: 1, p: 2, overflowY: "auto", bgcolor: "#f9fbf9" } },
      messages.map((m, idx) => e(MessageBubble, { key: idx, message: m })),
      e("div", { ref: endRef })
    ),
    e(Box, { sx: { px: 2, py: 1, display: "flex", gap: 1, flexWrap: "wrap", bgcolor: "#f1f8e9" } },
      SUGGESTIONS.map((s, idx) => e(Chip, {
        key: idx, label: s, size: "small", color: "success", variant: "outlined",
        clickable: !sending, onClick: () => handleSend(s)
      }))
    ),
    e(Box, { sx: { p: 2, bgcolor: "#ffffff", display: "flex", gap: 1 } },
      e(TextField, {
        fullWidth: true, placeholder: "Hỏi thông tin thuốc, vắc-xin, liều dùng, báo giá thú y...",
        value: text, disabled: sending, onChange: (evt) => setText(evt.target.value),
        onKeyDown: (evt) => { if (evt.key === "Enter" && !evt.shiftKey) { evt.preventDefault(); handleSend(); } }
      }),
      e(Button, { variant: "contained", color: "success", disabled: !text.trim() || sending, onClick: () => handleSend() }, "Gửi")
    )
  );
}
