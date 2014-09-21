'use strict';

angular.module('deathmsgServices', ['ngResource', 'ngRoute', 'ngSanitize'])
  .factory('Post', function($http) {
    return {
      postPhone: function(form) {
        return $http.post('/save-phone', form, {
          headers: {'Content-Type': undefined},
          transformRequest: angular.identity
        });
      }
    }
  });
