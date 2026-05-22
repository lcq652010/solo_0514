const webpack = require('webpack')
const { merge } = require('webpack-merge')
const baseConfig = require('./webpack.base.conf.js')

module.exports = merge(baseConfig, {
  mode: 'development',
  devServer: {
    port: 8081,
    hot: true,
    open: true,
    historyApiFallback: true
  },
  devtool: 'eval-cheap-module-source-map',
  plugins: [
    new webpack.DefinePlugin({
      'process.env': {
        NODE_ENV: '"development"'
      }
    })
  ]
})
