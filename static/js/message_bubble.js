const e = React.createElement;
const { Box, Paper, Typography, Button } = MaterialUI;

export function MessageBubble({ message }) {
  const isUser = message.role === "human";
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    if (navigator.clipboard) {
      navigator.clipboard.writeText(message.content);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  return e(
    Box,
    { sx: { display: "flex", justifyContent: isUser ? "flex-end" : "flex-start", mb: 2 } },
    e(
      Paper,
      {
        elevation: 1,
        sx: {
          p: 1.8,
          maxWidth: "80%",
          borderRadius: 2.5,
          bgcolor: isUser ? "#2e7d32" : "#ffffff",
          color: isUser ? "#ffffff" : "#212121",
          whiteSpace: "pre-wrap",
        },
      },
      e(Typography, { variant: "body1", sx: { lineHeight: 1.6 } }, message.content),
      !isUser && e(
        Box,
        { sx: { display: "flex", justifyContent: "flex-end", mt: 1 } },
        e(
          Button,
          {
            size: "small",
            sx: { fontSize: "0.75rem", color: "#558b2f", textTransform: "none" },
            onClick: handleCopy
          },
          copied ? "✓ Đã sao chép" : "📋 Sao chép đơn"
        )
      )
    )
  );
}
