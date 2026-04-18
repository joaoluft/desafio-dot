import { useState } from "react";

export default function InputBar({ onSend, loading }) {
  const [text, setText] = useState("");

  function handleSend() {
    const trimmed = text.trim();
    if (!trimmed || loading) return;
    onSend(trimmed);
    setText("");
  }

  function handleKeyDown(e) {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  }

  return (
    <div
      style={{
        display: "flex",
        gap: 8,
        padding: "12px 16px",
        borderTop: "1px solid #e0e0e0",
        backgroundColor: "#fff",
      }}
    >
      <input
        type="text"
        value={text}
        onChange={(e) => setText(e.target.value)}
        onKeyDown={handleKeyDown}
        disabled={loading}
        placeholder="Digite sua mensagem..."
        style={{
          flex: 1,
          padding: "10px 14px",
          borderRadius: 20,
          border: "1px solid #d0d0d0",
          fontSize: 14,
          outline: "none",
          backgroundColor: loading ? "#f5f5f5" : "#fff",
        }}
      />
      <button
        onClick={handleSend}
        disabled={loading || !text.trim()}
        style={{
          padding: "10px 18px",
          borderRadius: 20,
          border: "none",
          backgroundColor: loading || !text.trim() ? "#b0c4de" : "#0084ff",
          color: "#fff",
          fontSize: 14,
          cursor: loading || !text.trim() ? "not-allowed" : "pointer",
          fontWeight: 600,
        }}
      >
        {loading ? "…" : "Enviar"}
      </button>
    </div>
  );
}
