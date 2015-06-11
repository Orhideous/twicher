gulp       = require 'gulp'
uglify     = require 'gulp-uglify'
stylus     = require 'gulp-stylus'
rename     = require 'gulp-rename'
gutil      = require 'gulp-util'
source     = require 'vinyl-source-stream'
buffer     = require 'vinyl-buffer'
browserify = require 'browserify'
del        = require 'del'
pkginfo    = require './package.json'

gulp.task 'build', ['build:scripts', 'build:stylesheets']

gulp.task 'build:scripts', ->
  browserify
    entries: pkginfo.assets.scripts.entries
    paths: pkginfo.assets.scripts.paths
  .bundle()
  .pipe source 'bundle.js'
  .pipe buffer()
  .pipe if gutil.env.type is 'production' then uglify() else gutil.noop()
  .pipe gulp.dest pkginfo.dist

gulp.task 'build:stylesheets', ->
  gulp.src pkginfo.assets.stylesheets
    .pipe stylus
      compress: true,
      include: pkginfo.stylus.includes
    .pipe rename 'bundle.css'
    .pipe gulp.dest pkginfo.dist

gulp.task 'watch', ['build'], ->
  gulp.watch pkginfo.assets.scripts.watches, ['build:scripts']
  gulp.watch pkginfo.assets.stylesheets, ['build:stylesheets']

gulp.task 'clean', (cb) ->
  del ['#{pkginfo.dist}/*', '!.gitignore'], cb
