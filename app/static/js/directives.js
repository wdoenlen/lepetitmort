'use strict';

/* Directives */

angular.module('deathmsgDirectives', [])
  .directive('blurMe', function($timeout) {
    return {
      scope: { trigger: '@blurMe' },
      link: function(scope, element) {
        scope.$watch('trigger', function(value) {
          if(value === "true") {
            $timeout(function() {
              element[0].blur();
            });
          }
        });
      }
    };
  });