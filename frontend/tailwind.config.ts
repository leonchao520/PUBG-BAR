import type { Config } from "tailwindcss";

export default {
  content: [
    "./components/**/*.{vue,js,ts}",
    "./layouts/**/*.vue",
    "./pages/**/*.vue",
    "./app.vue",
    "./error.vue",
  ],
  theme: {
    extend: {
      colors: {
        pubg: {
          dark: "#1a1a2e",
          card: "#16213e",
          "card-hover": "#1e2a4a",
          accent: "#f5a623",
          "accent-hover": "#e09612",
          green: "#48bb78",
          red: "#e53e3e",
          muted: "#a0aec0",
          border: "#2a3a5c",
        },
      },
      fontFamily: {
        military: ['"Inter"', '"Segoe UI"', "sans-serif"],
      },
    },
  },
  plugins: [],
} satisfies Config;
