import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    // This setting is good practice for development tools like ngrok
    allowedHosts: 'all', 
    proxy: {
      '/terminal': {
        target: 'ws://localhost:3001',
        ws: true,
      },
    }
  }
})