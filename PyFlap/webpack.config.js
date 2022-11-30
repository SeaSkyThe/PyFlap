const path = require('path');

module.exports = {
    entry: './static/js/finiteautomata/fa.js',
    output: {
        filename: 'index.js',
        path: path.resolve('./static/js/', 'finiteautomata'),
    },
};