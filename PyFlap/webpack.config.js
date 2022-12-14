const path = require('path');

module.exports = {
    mode: 'production',
    entry: './static/js/finiteautomata/fa.js',
    output: {
        filename: 'index.js',
        path: path.resolve('./static/js/', 'finiteautomata'),
    },
    experiments: {
        topLevelAwait: true
    },
};