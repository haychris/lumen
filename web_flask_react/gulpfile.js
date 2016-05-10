'use strict';

// requirements

var gulp = require('gulp'),
    browserify = require('gulp-browserify'),
    size = require('gulp-size'),
    clean = require('gulp-clean');


// tasks

gulp.task('transform', function () {
  gulp.src('./project/static/scripts/jsx/indexJSX.js')
    .pipe(browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./project/static/scripts/js'))
    .pipe(size());

  return gulp.src('./project/static/scripts/jsx/courseHistInputJSX.js')
    .pipe(browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./project/static/scripts/js'))
    .pipe(size());
});

gulp.task('transform_results', function () {
  return gulp.src('./project/static/scripts/jsx/results.js')
    .pipe(browserify({transform: ['reactify']}))
    .pipe(gulp.dest('./project/static/scripts/js'))
    .pipe(size());
});


gulp.task('clean', function () {
  return gulp.src(['./project/static/scripts/js'], {read: false})
    .pipe(clean());
});

gulp.task('default', ['clean'], function() {
  gulp.start('transform');
  gulp.watch('./project/static/scripts/jsx/courseHistInputJSX.js', ['transform']);
  gulp.watch('./project/static/scripts/jsx/indexJSX.js', ['transform']);
});
