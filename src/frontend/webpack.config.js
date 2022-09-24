const path = require('path')
const CssMinimizerPlugin = require('css-minimizer-webpack-plugin')
const MiniCssExtractPlugin = require('mini-css-extract-plugin')
const CopyPlugin = require('copy-webpack-plugin')
const TerserPlugin = require("terser-webpack-plugin");

const config = {
  entry: {
    index: path.resolve(__dirname, 'index.js'),
  },
  output: {
    path: path.resolve(__dirname, '..', 'hanusovedni', 'static', 'dist'),
    publicPath: '',
  },
  module: {
    rules: [
      {
        test: /\.scss$/,
        use: [
          MiniCssExtractPlugin.loader,
          'css-loader',
          'resolve-url-loader',
          {
            loader: 'sass-loader',
            options: {
              sourceMap: true
            }
          }
        ]
      },
      {
        test: /\.js$/,
        exclude: /(node_modules|bower_components)/,
        use: {
          loader: 'babel-loader',
          options: {
            presets: ['@babel/preset-env']
          }
        }
      },
      {
        test: /\.(png|svg|jpg|jpeg|gif)$/i,
        type: 'asset/resource',
      },
      {
        test: /\.(woff|woff2|eot|ttf|otf)$/i,
        include: path.resolve(__dirname, 'fonts'),
        type: 'asset/resource',
      },
    ]
  },
  plugins: [
    new MiniCssExtractPlugin({
      filename: 'bundle.css'
    }),
    new CopyPlugin({
      patterns: [
        {from: './elm/elm-bundle.js', to: 'elm-bundle.js'},
      ],
    }),
  ],
  devServer: {
    proxy: {
      '/': 'http://localhost:8000',
    },
    hot: true
  }
}

module.exports = (env, argv) => {
  if (argv.mode === 'development') {
    config.devtool = 'source-map'
  }

  if (argv.mode === 'production') {
    config.optimization = {
      minimize: true,
      minimizer: [
        `...`,
        new TerserPlugin(),
        new CssMinimizerPlugin(),
      ],
    }
  }

  return config
}
