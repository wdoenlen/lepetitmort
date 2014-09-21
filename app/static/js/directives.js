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
        elem.bind('keydown', function(e) {
          var char = String.fromCharCode(e.which||e.charCode||e.keyCode);
          if (!(e.keyCode == 8) && (!isNumber(char) || isGE(scope.phoneNumber, 10))) {
            e.preventDefault();
          }
        });
        if (!ctrl) {return;}
        ctrl.$parsers.unshift(function (viewValue) {
          viewValue = viewValue.trim();
          var plainNumber = viewValue.replace(/[^\d+]/g, '');
          if (viewValue.charAt(viewValue.length - 1) == '-') {
            plainNumber = plainNumber.slice(0, plainNumber.length - 1);
          }
          elem.val(getFormattedPhone(plainNumber));
          return plainNumber;
        });
      }
    };
  }]);

var getFormattedPhone = function(str) {
  var len = str.length;
  if (len < 3) {
    return str;
  } else if (len >= 3 && len < 6) {
    return '(' + str.slice(0, 3) + ') - ' + str.slice(3, len);
  } else if (len == 6) {
    return '(' + str.slice(0, 3) + ') - ' + str.slice(3, len) + ' - ';
  } else {
    return '(' + str.slice(0, 3) + ') - ' + str.slice(3, 6) + ' - ' + str.slice(6, len);
  }
}

var isNumber = function(char) {
  return ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9'].indexOf(char) > -1;
}

var isGE = function(txt, num) {
  if (!txt) {
    return false;
  }
  return txt.length >= num;
}
