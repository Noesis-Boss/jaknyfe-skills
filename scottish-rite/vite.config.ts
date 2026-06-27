import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
 plugins: [react()],
 base: '/scottish-rite/',
 build: {
   outDir: 'dist',
   base: "/", // ensure assets are served from root
   assetsDir: "assets",
 }
});