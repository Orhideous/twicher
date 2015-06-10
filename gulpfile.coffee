gulp       = require 'gulp'
uglify     = require 'gulp-uglify'
sourcemaps = require 'gulp-sourcemaps'
stylus     = require 'gulp-stylus'
rename     = require 'gulp-rename'
source     = require 'vinyl-source-stream'
buffer     = require 'vinyl-buffer'
browserify = require 'browserify'
del        = require 'del'
pkginfo    = require './package.json'

gulp.task 'build', ['build:scripts', 'build:stylesheets']

gulp.task 'build:scripts', () ->
  browserify(entries: pkginfo.assets.scripts, debug: true).bundle()
    .pipe(source('bundle.js'))
    .pipe(buffer())
    .pipe(sourcemaps.init(loadMaps: true))
    .pipe(uglify())
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(pkginfo.dist))

gulp.task 'build:stylesheets', () ->
  #bootstrap = require('bootstrap-styl')
  gulp.src(pkginfo.assets.stylesheets)
    .pipe(sourcemaps.init(loadMaps: true))
    .pipe(stylus(
      compress: true,
      include: pkginfo.stylus.includes
    ))
    .pipe(rename('bundle.css'))
    .pipe(sourcemaps.write())
    .pipe(gulp.dest(pkginfo.dist))

gulp.task 'watch', ['build'], () ->
  gulp.watch(pkginfo.assets.scripts, ['build:scripts'])
  gulp.watch(pkginfo.assets.stylesheets, ['build:stylesheets'])

gulp.task 'clean', (cb) ->
  del([pkginfo.dist + '/*', '!.gitignore'], cb)
