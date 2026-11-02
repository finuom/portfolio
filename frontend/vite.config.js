import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    // Em desenvolvimento, /api vai para o FastAPI local.
    proxy: { '/api': 'http://localhost:8000' },
  },
})
