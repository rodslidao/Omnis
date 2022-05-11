module.exports = {
  // ... other options
  node: {
    fs: 'empty',
  },
  module: {
    rules: [
      {
        enforce: 'pre',
        test: /\.(js|vue)$/,
        loader: 'eslint-loader',
        exclude: /node_modules/,
      },
    ],
  },
  resolve: {
    fallback: {
      path: require.resolve('path-browserify'),
      // path: false,
    },
  },
};
