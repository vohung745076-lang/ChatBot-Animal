# PROMPT P7: Giao Diện Người Dùng Web (Material UI & Vanilla JS Không Cần Build Step)

Dán TOÀN BỘ nội dung dưới đây vào công cụ AI lập trình (opencode / coding agent). Chỉ thực hiện P7 khi P6 đã hoàn tất và kiểm thử thành công.

---

# 1. Role (Vai trò):

Kỹ sư Frontend chuyên nghiệp về giao diện web Material UI (MUI) và Vanilla JavaScript (ES Modules).
Bạn thiết kế giao diện người dùng cho **VetChatbot - Trợ lý Tư Vấn Hàng Hóa Thú Y** chạy trực tiếp trên trình duyệt mà không cần bước biên dịch (No JSX, No Babel, No Webpack/Vite) thông qua React 18 UMD và Material UI UMD.
Bạn thiết kế giao diện mang phong cách y tế / thú y hiện đại (màu xanh lá y tế chủ đạo), trải nghiệm mượt mà, hỗ trợ đối thoại nhập khóa Google Gemini API lần đầu, và nghiêm cấm tuyệt đối việc sử dụng `innerHTML` để loại trừ hoàn toàn lỗ hổng XSS.

---

# 2. Context (5W1H):

* **What:** Xây dựng `static/index.html` cùng 10 file JavaScript trong `static/js/`:
  - `session_id.js`
  - `api_status.js`
  - `api_setup.js`
  - `api_chat.js`
  - `api_reset.js`
  - `message_bubble.js`
  - `setup_dialog.js`
  - `chat_view.js`
  - `send_handler.js`
  - `main.js`
* **Why:** Đơn giản hóa tối đa quy trình chạy cho người dùng và học viên (chỉ cần chạy server Python là mở trình duyệt dùng được ngay, không cần cài đặt Node.js hay npm). Việc chia nhỏ module và tuân thủ mỗi file dưới 100 dòng giúp mã nguồn cực kỳ dễ bảo trì và mở rộng.
* **Who/Where:** Thư mục `static/` của dự án `chatbot/`.
* **When:** Thực hiện sau P6 và trước P8 (System Prompt & Kịch bản chạy thử).
* **How:** Viết các component bằng `React.createElement`, gọi API qua hàm `fetch`, bắt lỗi mạng thành object `{ok, status, data}` thân thiện.
* **Ràng buộc:** Cấm `innerHTML`, cấm `dangerouslySetInnerHTML`; mỗi file dưới 100 dòng; không lưu API Key vào `localStorage`.

---

# 3. Instructions (formal-spec):

## 3a. Điều kiện và Bất biến (PRE, POST, INV)

### PRE:
- PRE.1: Thư mục `static/js/` đã có sẵn từ P1.
- PRE.2: Server Flask ở P6 đã sẵn sàng phục vụ static files.

### POST:
- POST.1: `static/index.html` và 10 tệp trong `static/js/` được tạo đầy đủ.
- POST.2: Tất cả các file JS đều dưới 100 dòng và không chứa từ khóa `innerHTML`.
- POST.3: Giao diện mở được trên Chrome/Edge tại `http://127.0.0.1:2610`.

### INV:
- INV.1: Giao diện hiển thị tiếng Việt có dấu đầy đủ, chuẩn văn phong tư vấn thú y.
- INV.2: Khóa API chỉ được gửi qua `POST /api/setup`, không bao giờ ghi vào `localStorage` hay in ra `console.log`.

---

# 4. Đặc Tả Chi Tiết Các Tệp Mã Nguồn

### 1. `static/index.html`
```html
<!DOCTYPE html>
<html lang="vi">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>VetChatbot - Tư Vấn Hàng Hóa Thú Y</title>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Roboto:300,400,500,700&display=swap" />
  <link rel="stylesheet" href="https://fonts.googleapis.com/icon?family=Material+Icons" />
  <script src="https://unpkg.com/react@18/umd/react.production.min.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.production.min.js"></script>
  <script src="https://unpkg.com/@mui/material@5.15.14/umd/material-ui.production.min.js"></script>
  <style>
    body { margin: 0; background-color: #f4f6f8; font-family: Roboto, sans-serif; }
    #root { display: flex; justify-content: center; height: 100vh; }
  </style>
</head>
<body>
  <div id="root"></div>
  <script type="module" src="/static/js/main.js"></script>
</body>
</html>
```

### 2. `static/js/session_id.js`
```javascript
export function getSessionId() {
  let sid = localStorage.getItem("vet_session_id");
  if (!sid) {
    sid = "vet-" + crypto.randomUUID().slice(0, 18);
    localStorage.setItem("vet_session_id", sid);
  }
  return sid;
}
```

### 3. `static/js/api_status.js`
```javascript
export async function apiStatus() {
  try {
    const res = await fetch("/api/setup/status");
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Không thể kết nối máy chủ" } };
  }
}
```

### 4. `static/js/api_setup.js`
```javascript
export async function apiSetup(apiKey) {
  try {
    const res = await fetch("/api/setup", {
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
```

### 5. `static/js/api_chat.js`
```javascript
export async function apiChat(sessionId, message) {
  try {
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ session_id: sessionId, message }),
    });
    const data = await res.json();
    return { ok: res.ok, status: res.status, data };
  } catch (e) {
    return { ok: false, status: 0, data: { message: "Không thể kết nối đến máy chủ" } };
  }
}
```

### 6. `static/js/api_reset.js`
```javascript
export async function apiReset(sessionId) {
  try {
    const res = await fetch("/api/reset", {
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
```

### 7. `static/js/message_bubble.js`
```javascript
const e = React.createElement;
const { Box, Paper, Typography } = MaterialUI;

export function MessageBubble({ message }) {
  const isUser = message.role === "human";
  return e(
    Box,
    { sx: { display: "flex", justifyContent: isUser ? "flex-end" : "flex-start", mb: 2 } },
    e(
      Paper,
      {
        elevation: 1,
        sx: {
          p: 1.8,
          maxWidth: "75%",
          borderRadius: 2.5,
          bgcolor: isUser ? "#2e7d32" : "#ffffff",
          color: isUser ? "#ffffff" : "#212121",
          whiteSpace: "pre-wrap",
        },
      },
      e(Typography, { variant: "body1" }, message.content)
    )
  );
}
```

### 8. `static/js/setup_dialog.js`
```javascript
const e = React.createElement;
const { Dialog, DialogTitle, DialogContent, DialogActions, TextField, Button, Alert } = MaterialUI;

export function SetupDialog({ open, onSave, errorMsg, loading }) {
  const [key, setKey] = React.useState("");

  return e(
    Dialog,
    { open, maxWidth: "sm", fullWidth: true },
    e(DialogTitle, null, "Cấu Hình Google Gemini API Key"),
    e(
      DialogContent,
      null,
      errorMsg ? e(Alert, { severity: "error", sx: { mb: 2 } }, errorMsg) : null,
      e(TextField, {
        autoFocus: true,
        margin: "dense",
        label: "Khóa Google Gemini API (AIzaSy...)",
        type: "password",
        fullWidth: true,
        variant: "outlined",
        value: key,
        onChange: (evt) => setKey(evt.target.value),
        helperText: "Khóa sẽ được lưu an toàn trong file .env cục bộ",
      })
    ),
    e(
      DialogActions,
      null,
      e(
        Button,
        {
          variant: "contained",
          color: "success",
          disabled: !key.trim() || loading,
          onClick: () => { onSave(key); setKey(""); },
        },
        loading ? "Đang lưu..." : "Lưu & Bắt đầu"
      )
    )
  );
}
```

### 9. `static/js/chat_view.js`
```javascript
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
```

### 10. `static/js/send_handler.js`
```javascript
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
```

### 11. `static/js/main.js`
```javascript
const e = React.createElement;
const { createRoot } = ReactDOM;
import { apiReset } from "./api_reset.js";
import { apiSetup } from "./api_setup.js";
import { apiStatus } from "./api_status.js";
import { ChatView } from "./chat_view.js";
import { handleSendMessage } from "./send_handler.js";
import { getSessionId } from "./session_id.js";
import { SetupDialog } from "./setup_dialog.js";

function App() {
  const sid = React.useMemo(() => getSessionId(), []);
  const [messages, setMessages] = React.useState([
    { role: "ai", content: "Xin chào! Tôi là VetChatbot. Tôi có thể hỗ trợ tư vấn thông tin về thuốc, vắc-xin, dinh dưỡng và hàng hóa thú y nào cho bạn?" }
  ]);
  const [dialogOpen, setDialogOpen] = React.useState(false);
  const [dialogError, setDialogError] = React.useState("");
  const [loading, setLoading] = React.useState(false);
  const [sending, setSending] = React.useState(false);

  React.useEffect(() => {
    apiStatus().then((res) => {
      if (res.ok && !res.data.configured) setDialogOpen(true);
    });
  }, []);

  const onSaveKey = async (key) => {
    setLoading(true);
    const res = await apiSetup(key);
    setLoading(false);
    if (res.ok) {
      setDialogOpen(false);
      setDialogError("");
    } else {
      setDialogError(res.data?.message || "Lỗi lưu khóa");
    }
  };

  const onReset = async () => {
    await apiReset(sid);
    setMessages([{ role: "ai", content: "Đã làm mới cuộc trò chuyện thú y." }]);
  };

  return e(React.Fragment, null,
    e(ChatView, {
      messages,
      sending,
      onSend: (text) => handleSendMessage({ sid, text, setMessages, setSending, openSetup: (msg) => { setDialogError(msg); setDialogOpen(true); } }),
      onReset
    }),
    e(SetupDialog, { open: dialogOpen, onSave: onSaveKey, errorMsg: dialogError, loading })
  );
}

createRoot(document.getElementById("root")).render(e(App));
```
