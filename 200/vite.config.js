const vue = require('@vitejs/plugin-vue2')
const path = require('path')

module.exports = {
  plugins: [vue()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, 'src')
    }
  }
}
