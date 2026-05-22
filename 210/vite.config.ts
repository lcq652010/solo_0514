import { defineConfig } from 'vite'
import { createVuePlugin as vue } from 'vite-plugin-vue2'
import path from 'path'

export default defineConfig({
  build: {
    sourcemap: 'hidden',
  },
  plugins: [
    vue(),
  ],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
      vue: 'vue/dist/vue.esm.js',
    },
    extensions: ['.js', '.ts', '.vue', '.json'],
  },
})
