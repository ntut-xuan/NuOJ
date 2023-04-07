const path = require("path");
var CopyWebpackPlugin = require("copy-webpack-plugin");

module.exports = {
  context: path.resolve(__dirname, "src"),
  entry: {
    submission: "js/submission_list.jsx",
  },
  mode: "development",
  // mode: "production",
  output: {
    filename: "[name].js",
    path: path.resolve(__dirname, "static/js"),
  },
  module: {
    rules: [
      {
        test: /\.jsx$/,
        exclude: /node_modules/,
        use: {
          loader: "babel-loader",
          options: {
            presets: [["@babel/preset-react"]],
          },
        },
      },
      {
        test: /\.css/,
        use: ["style-loader", "css-loader"],
      },
    ],
  },
  devServer: {
    static: [
      {
        directory: path.join(__dirname, "static"),
        publicPath: "/static",
      },
      {
        directory: path.join(__dirname, "templates"),
        publicPath: "/",
      },
    ],
    compress: true,
    port: 9000,
  },
  plugins: [
    new CopyWebpackPlugin({
      patterns: [
        {
          from: path.resolve(__dirname, "./src/js", "mockServiceWorker.js"),
          to: "mockServiceWorker.js",
        },
      ],
    }),
  ],
};
