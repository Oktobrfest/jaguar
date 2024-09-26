const ReactRefreshWebpackPlugin = require(
    '@pmmmwh/react-refresh-webpack-plugin');
const webpack = require('webpack');
const path = require('path');

const isDevelopment = process.env.NODE_ENV !== 'production';


const config = {
    mode: 'development',
    entry: path.join(__dirname, '/scripts/index.tsx'),
    output: {
        path: path.join(__dirname, '/scripts/dist'),
        filename: 'bundle.js',
    },
    devtool: 'eval-source-map',
    resolve: {
        extensions: ['.ts', '.tsx', '.js', '.jsx', '.css'],
        alias: {
            '~': path.resolve(__dirname, 'node_modules')
        },
        modules: ['node_modules']
    },
    module: {
        rules: [
            {
                test: /\.(js|jsx|ts|tsx)$/,
                exclude: /node_modules/,
                use: {
                    loader: 'babel-loader',
                    options: {
                        presets: ['@babel/preset-react',
                            '@babel/preset-typescript'],
                        rootMode: "upward",
                        plugins: [isDevelopment &&
                        require.resolve('react-refresh/babel')].filter(Boolean),
                    },
                },
            },
            {
                test: /\.css$/,
                use: ['style-loader', 'css-loader']
            },
            {
                test: /\.(png|svg|jpg|gif)$/,
                use: 'file-loader'
            }
        ]
    },
    optimization: {
        minimize: false
    },
    devServer: {
        hot: true, // Enable HMR on webpack-dev-server
        liveReload: false  // NOT SURE IF THIS IS RIGHT WAY TO DO OR NOT
    },
    plugins: [
        isDevelopment ? new webpack.HotModuleReplacementPlugin() : null,
        isDevelopment ? new ReactRefreshWebpackPlugin() : null
    ].filter(Boolean),
    resolveLoader: {
        modules: ['node_modules']
    },
    context: path.resolve(__dirname, 'app/static'),
    stats: {
        errorDetails: true,
        modules: true,    
        reasons: true      // Display the reasons about why modules are included
    }


};

// console.log('Resolved path:', path.resolve(__dirname, 'node_modules'));
// console.log('Webpack Resolve Config:', config.resolve);
// console.log('Webpack Module Rules:', config.module.rules);


module.exports = config;
