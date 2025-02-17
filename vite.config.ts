import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['lucide-react'],
  },
  server: {
    watch: {
      ignored: ['**/cloned_repos/**'], // ✅ Ignore cloned repos to prevent unnecessary reloads
    },
  },
});
