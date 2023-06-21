import { defineConfig } from "vite";
import { resolve } from "path";
import react from "@vitejs/plugin-react-swc";
import Pages from "vite-plugin-pages";

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [
    react(),
    Pages({
      pagesDir: [{ dir: "./src/pages", baseRoute: "" }],
      exclude: ["**/compoments/*.jsx"],
    }),
  ],
});
