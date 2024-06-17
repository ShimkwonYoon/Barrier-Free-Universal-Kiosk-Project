const path = require("path");
const webpack = require("webpack");
const TerserPlugin = require("terser-webpack-plugin");
const HTMLWebpackPlugin = require("html-webpack-plugin");
const MiniCssExtractPlugin = require("mini-css-extract-plugin");
const CssMinimizerPlugin = require("css-minimizer-webpack-plugin");
const CleanWebpackPlugin = require("clean-webpack-plugin");

exports.default = {
    entry: {
        /** index.html 과 index.js를 포함하여 테스트할 경우 **/
        index: path.resolve(__dirname, "src", "index.js"),

        /** WebGLPlayer.js을 Library로 build할 경우 **/
        // index: path.resolve(__dirname, "src/libs", "WebGLPlayer.js"),

        /** Interface가 필요할 경우 **/
        // index: path.resolve(__dirname, "src/libs", "userInterface.js"),

        /** Worker가 필요할 경우 **/
        loadingWorker: path.resolve(__dirname, "src/libs/workers", "LoadingWorker.js"),
    },
    plugins: [
        /** index.html 과 index.js를 포함하여 테스트할 경우 아래 주석을 풀고 실행 **/
        new HTMLWebpackPlugin({
            template: path.resolve(__dirname, "src", "index.html"),
            inject: true,
        }),
        new MiniCssExtractPlugin(),
    ],
    optimization: {
        // runtimeChunk: "single",
        // minimize: false,
        minimize: true,
        minimizer: [
            new TerserPlugin({
                include: /\.min\.js$/,
                terserOptions: {},

                /** Library로 build할 경우 **/
                // minify: TerserPlugin.esbuildMinify,
            }),
            new CssMinimizerPlugin(),
        ],
    },
    module: {
        rules: [
            {
                test: /\.css$/,
                use: [MiniCssExtractPlugin.loader, "css-loader"],
            },
            {
                test: /\.scss$/,
                use: ["style-loader", "css-loader", "sass-loader"],
            },
            {
                test: /\.js$/,
                exclude: /node_modules/,
                use: ["babel-loader"],
                resolve: {
                    fullySpecified: false,
                },
            },
            {
                test: /\.(png|svg|jpe?g|gif)$/,
                loader: "url-loader",
                options: {
                    name: "[hash].[ext]",
                },
            },
            {
                test: /\.(woff|woff2|eot|ttf|otf)$/,
                loader: "url-loader",
            },
            {
                test: /\.ts$/,
                loader: "babel-loader",
                exclude: /node_modules/,
            },
        ],
    },
    resolve: {
        extensions: [".js", ".jsx", ".ts", ".tsx", ".json"],
    },
    output: {
        // /** Library로 build할 경우 **/
        // library: {
        //     /** Script에서 파일을 로딩하여 import 없이 사용할 경우 **/
        //     name: "WebGLPlayerLibrary",
        //     type: "umd",
        //     umdNamedDefine: true,

        //     /** Script에서 import를 사용하여 모듈을 로딩할 경우 **/
        //     // type: "module",
        // },

        path: path.resolve(__dirname, "public"),
        filename: "[name].min.js",
    },
    performance: {
        hints: false,
        maxEntrypointSize: 5120000,
        maxAssetSize: 5120000,
    },

    /** Source Map options **/
    // devtool: "hidden-source-map",

    /** Script에서 import(es6 문법)를 사용하여 모듈을 로딩할 경우 **/
    // experiments: {
    //     outputModule: true
    // }
};
