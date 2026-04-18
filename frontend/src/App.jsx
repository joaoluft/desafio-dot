import { useRef, useState } from "react";
import ChatWindow from "./components/ChatWindow";
import InputBar from "./components/InputBar";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8001";

export default function App() {
  // session persiste enquanto a aba estiver aberta — reseta ao recarregar
  const sessionId = useRef(crypto.randomUUID());
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  async function handleSend(text) {
    setMessages((prev) => [...prev, { role: "user", content: text, sources: [] }]);
    setLoading(true);

    try {
      const res = await fetch(`${API_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ session_id: sessionId.current, message: text }),
      });

      if (!res.ok) throw new Error(`HTTP ${res.status}`);

      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: data.answer, sources: data.sources ?? [] },
      ]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { role: "bot", content: "Erro ao conectar com o servidor.", sources: [] },
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div
      style={{
        display: "flex",
        flexDirection: "column",
        height: "100vh",
        maxWidth: 700,
        margin: "0 auto",
        fontFamily: "system-ui, sans-serif",
        boxShadow: "0 0 20px rgba(0,0,0,0.08)",
      }}
    >
      <header
        style={{
          padding: "16px 20px",
          backgroundColor: "#0084ff",
          color: "#fff",
          fontSize: 18,
          fontWeight: 700,
        }}
      >
        AI Assistant
      </header>
      <ChatWindow messages={messages} />
      <InputBar onSend={handleSend} loading={loading} />
    </div>
  );
}
