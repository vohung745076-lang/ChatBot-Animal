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
