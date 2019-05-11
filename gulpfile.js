const { src, dest, watch, series, parallel } = require('gulp')
const sass = require('gulp-sass')
const browserSync = require('browser-sync').create()

function css() {
  return src('./hanusovedni/static/sass/**/*.scss')
    .pipe(sass({outputStyle: 'compressed'}).on('error', sass.logError))
    .pipe(dest('./hanusovedni/static/css/'))
    .pipe(browserSync.stream())
}

function watchFiles() {
  watch('./hanusovedni/static/sass/**/*.scss', {ignoreInitial: false}, css)
  watch(['./hanusovedni/templates/**/*.html', './home/templates/**/*.html']).on('change', browserSync.reload)
}

function serve() {
  browserSync.init({
    proxy: "localhost:8000",
    port: 8888,
  })
  watchFiles()
}


exports.build = series(css)
exports.watch = watchFiles
exports.serve = serve
exports.default = serve
