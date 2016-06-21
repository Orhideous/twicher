var ExtractTextPlugin, isProduction, keys, path, vendors, webpack;

path = require('path');

webpack = require('webpack');

keys = require('lodash').keys;

ExtractTextPlugin = require('extract-text-webpack-plugin');

isProduction = process.env.NODE_ENV === 'production';

vendors = ["lodash", "react", "react-dom", "rx"];

var stylusSettings = {
    paths: [
        "node_modules/bootstrap-styl",
        "node_modules/react-quill/node_modules/quill"
    ],
    "resolve url": 1,
    "include css": 1
};

module.exports = {
    context: path.join(__dirname, 'frontend'),
    cache: true,
    devtool: "#source-map",
    entry: {
        main: "./main",
        vendor: vendors
    },
    output: {
        path: path.join(__dirname, 'twicher', 'static'),
        publicPath: "./",
        filename: '[name].bundle.js'
    },
    module: {
        noParse: /node_modules\/quill\/dist/,
        loaders: [
            {
                test: /\.jsx?$/,
                exclude: /(node_modules)/,
                loader: 'babel',
                query: {
                    presets: ['react', 'es2015']
                }
            },
            {
                test: /\.styl$/,
                loader: ExtractTextPlugin.extract(
                    "style-loader",
                    "css!stylus?" + JSON.stringify(stylusSettings)
                )
            },
            {
                test: /\.woff(2)?(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "url",
                query: {
                    limit: 10000,
                    mimetype: 'application/font-woff'
                }
            },
            {
                test: /\.(ttf|eot|svg)(\?v=[0-9]\.[0-9]\.[0-9])?$/,
                loader: "file"
            }
        ]
    },
    resolve: {
        extensions: ['', '.js', '.styl',],
        modulesDirectories: ['node_modules', 'scripts']
    },
    plugins: Array.prototype.concat(
        isProduction ? [new webpack.optimize.UglifyJsPlugin()] : [],
        [
            new ExtractTextPlugin("styles.css"),
            new webpack.optimize.CommonsChunkPlugin({
                name: 'vendor',
                minChunks: Infinity
            })
        ])
};