module.exports = function(grunt) {
  grunt.initConfig({
    meta: {
      version: '0.1.0'
    },
    banner: '/*! lpgray-site <%= grunt.template.today("yyyy-mm-dd") %> */\r\n',
    concat: {
      options: {
        banner: '<%= banner %>',
        stripBanners: true
      },
      jslib: {
        src: ['js/src/plugins/gtmap.formvalidate.js',
              'js/src/base.js'],
        dest: 'build/js/lpgray.js'
      }
    },
    uglify: {
      options: {
        banner: '<%= banner %>'
      },
      js: {
        src: '<%= concat.jslib.dest %>',
        dest: 'build/js/lpgray_<%= grunt.template.today("yyyymmdd") %>.min.js'
      }
    }
  });
  
  grunt.loadNpmTasks('grunt-contrib-concat');
  grunt.loadNpmTasks('grunt-contrib-uglify');
  
  grunt.registerTask('build', ['concat', 'uglify']);
};