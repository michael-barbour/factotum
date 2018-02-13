var path = require('path');
var webpack = require('webpack');
var BundleTracker = require('webpack-bundle-tracker');

module.exports = {
    context: __dirname,
    entry: ['./assets/js/index.jsx','./assets/js/search.jsx'],
    // entry: './assets/js/index.jsx',
    output: {
        path: path.resolve('./assets/bundles/'),
        filename: "[name].js"
    },

    plugins: [
        new BundleTracker({filename: './webpack-stats.json'})
    ]
};
