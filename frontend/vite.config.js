import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    // proxy para dev local sem CORS — só usado no `npm run dev`, não no Docker
    proxy: {
      "/chat": "http://localhost:8001",
    },
  },
});
