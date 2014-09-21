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
  })
  .directive('phoneformat', ['$filter', function($filter) {
    return {
      require: '?ngModel',
      link: function (scope, elem, attrs, ctrl) {
        if (!ctrl) return;
        ctrl.$parsers.unshift(function (viewValue) {
          var plainNumber = viewValue.replace(/[^\d+]/g, '');
          var st = plainNumber.toString();
          if (st.length >= 10) {
            st = st.substring(0,10);
          }
          elem.val(getFormattedPhone(st));
          return parseInt(st);
        });
      }
    };
  }]);

var getFormattedPhone = function(str) {
  var len = str.length;
  if (len < 3) {
    return str;
  } else if (len >= 3 && len <= 6) {
    return '(' + str.slice(0,3) + ') - ' + str.slice(3);
  } else {
    return '(' + str.slice(0,3) + ') - ' + str.slice(3,6) + ' - ' + str.slice(6,10)
  }
}
