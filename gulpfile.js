const { src, dest, watch, series, parallel } = require('gulp')
const sass = require('gulp-sass')
const browserSync = require('browser-sync').create()
const elm = require('gulp-elm')
const plumber = require('gulp-plumber')
const notify = require('gulp-notify')

function css () {
  return src('./src/hanusovedni/static/sass/style.scss')
    .pipe(sass({ outputStyle: 'compressed' }).on('error', sass.logError))
    .pipe(dest('./src/hanusovedni/static/css/'))
    .pipe(browserSync.stream())
}

function logErrorHandler (err) {
  console.log(err)
  notify.onError({
    title: 'Gulp',
    subtitle: 'Failure!',
    message: 'Error: <%= error.message %>',
    sound: 'Beep'
  })(err)
  this.emit('end')
}

function compileElm () {
  return src('./src/hanusovedni/static/elm/src/Main.elm')
    .pipe(plumber({ errorHandler: logErrorHandler }))
    .pipe(elm.bundle('bundle.js', { optimize: true, cwd: './src/hanusovedni/static/elm' }))
    .pipe(dest('./src/hanusovedni/static/elm/'))
  // .pipe(browserSync.reload())
}

function watchFiles () {
  watch('./src/hanusovedni/static/sass/**/*.scss', { ignoreInitial: false }, css)
  watch('./src/hanusovedni/static/js/**/*.js').on('change', browserSync.reload)
  watch('./src/hanusovedni/static/elm/src/**/*.elm').on('change', compileElm)
  watch(['./src/hanusovedni/templates/**/*.html', './src/home/templates/**/*.html']).on('change', browserSync.reload)
}

function serve () {
  browserSync.init({
    proxy: 'localhost:8000',
    port: 8888,
  })
  watchFiles()
}

exports.build = series(css)
exports.watch = watchFiles
exports.serve = serve
exports.default = serve
