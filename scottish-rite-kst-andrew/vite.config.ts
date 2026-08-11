import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

const deploySubpath = process.env.DEPLOY_SUBPATH?.replaceAll('/', '')

export default defineConfig({
  plugins: [react()],
  base: deploySubpath ? `/${deploySubpath}/` : '/',
  server: {
    host: '0.0.0.0',
    port: Number(process.env.PORT) || 5173,
  },
  build: {
    rollupOptions: {
      output: {
        assetFileNames: (assetInfo) => {
          if (assetInfo.name && assetInfo.name.endsWith('.png')) {
            return 'assets/[name]-[hash][extname]'
          }
          return 'assets/[name]-[hash][extname]'
        },
      },
    },
  },
})
