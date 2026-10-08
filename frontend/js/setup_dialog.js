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
        label: "Khóa Google Gemini API (AQ... hoặc AIzaSy...)",
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
