const {resolve} = require('path');
import { defineConfig } from 'vite'
import FullReload from 'vite-plugin-full-reload'


export default defineConfig({
  root: resolve('frontend'),
  base: '/static/',
  server: {
    host: '0.0.0.0',
    port: 3000,
    open: false,
    watch: {
      usePolling: true,
      disableGlobbing: false,
    },
  },
  resolve: {
    alias: {
      '~bootstrap': resolve(__dirname, 'node_modules/bootstrap'),
    }
  },
  plugins: [
    // FullReload(['hanusovedni/templates/**/*.html'])
  ],
  build: {
    outDir: resolve('frontend/static'),
    assetsDir: '',
    manifest: true,
    emptyOutDir: true,
    target: 'es2015',
    rollupOptions: {
      input: {
        main: resolve('frontend/main.js'),
      },
      output: {
        chunkFileNames: undefined,
      },
    },
  },
})
