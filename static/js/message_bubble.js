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
