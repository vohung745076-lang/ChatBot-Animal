const e = React.createElement;
const { Box, AppBar, Toolbar, Typography, IconButton, TextField, Button } = MaterialUI;
import { MessageBubble } from "./message_bubble.js";

export function ChatView({ messages, onSend, onReset, sending }) {
  const [text, setText] = React.useState("");
  const endRef = React.useRef(null);

  React.useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = () => {
    if (!text.trim() || sending) return;
    onSend(text);
    setText("");
  };

  return e(
    Box,
    { sx: { width: "100%", maxWidth: 880, height: "100vh", display: "flex", flexDirection: "column" } },
    e(AppBar, { position: "static", sx: { bgcolor: "#2e7d32" } },
      e(Toolbar, null,
        e(Typography, { variant: "h6", sx: { flexGrow: 1 } }, "🌿 VetChatbot - Tư Vấn Hàng Hóa Thú Y"),
        e(Button, { color: "inherit", onClick: onReset }, "Làm mới")
      )
    ),
    e(Box, { sx: { flexGrow: 1, p: 2, overflowY: "auto", bgcolor: "#f9fbf9" } },
      messages.map((m, idx) => e(MessageBubble, { key: idx, message: m })),
      e("div", { ref: endRef })
    ),
    e(Box, { sx: { p: 2, bgcolor: "#ffffff", display: "flex", gap: 1 } },
      e(TextField, {
        fullWidth: true,
        placeholder: "Hỏi thông tin thuốc, vắc-xin, liều dùng thú y...",
        value: text,
        disabled: sending,
        onChange: (evt) => setText(evt.target.value),
        onKeyDown: (evt) => { if (evt.key === "Enter" && !evt.shiftKey) { evt.preventDefault(); handleSend(); } }
      }),
      e(Button, { variant: "contained", color: "success", disabled: !text.trim() || sending, onClick: handleSend }, "Gửi")
    )
  );
}
