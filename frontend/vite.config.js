import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      "/api":           "http://localhost:5000",
      "/get_faqs":      "http://localhost:5000",
      "/clear_history": "http://localhost:5000",
      "/health":        "http://localhost:5000",
    },
  },
});