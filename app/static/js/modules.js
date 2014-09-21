'use strict';

angular.module('DeathMsg', ['deathmsgServices', 'deathmsgFilters', 'deathmsgDirectives', 'ui.bootstrap', 'angular-loading-bar'])
  .controller('main', function($scope) {

  })
  .controller('about', function($scope) {

  })
  .controller('home', function($scope, Post) {
    $scope.msg = null;
    $scope.isSuccessMsg = false;
    $scope.setMessage = function(obj) {
      $scope.msg = obj.msg;
      $scope.isSuccessMsg = obj.success;
    }

    $scope.submitPhone = function() {
      var phoneNumber = $scope.phoneNumber.toString().trim();
      if (phoneNumber.length == 10) {
        var form = new FormData();
        form.append('phone', phoneNumber);
        Post.postPhone(form).then(function(data) {
          console.log(data)
          $scope.setMessage({'msg':data.data.message, 'success':data.data.success})
        });
      } else {
        $scope.setMessage({'msg':'Please enter a complete phone number', 'success':false});
      }
    }

    $scope.$watch('phoneNumber', function(newval, oldval) {
      if ($scope.msg && newval != oldval) {
        $scope.msg = null;
      }
    })
  })
  .config([
    '$routeProvider', '$locationProvider',
    function($routeProvider, $locationProvider) {
      $routeProvider
	.when('/', {
	  templateUrl: '/static/partials/home.html',
          controller: 'home'
	})
        .when('/about', {
          templateUrl: '/static/partials/about.html',
          controller: 'about'
        })
	.otherwise({
	  redirectTo: '/'
	});
      $locationProvider.html5Mode(true);
    }
  ]);

function redirectIfNotArgs(params, $location) {
  for (var param in params) {
    if (!params[param] || params[param] == '') {
      $location.path('/')
    }
  }
}

var sliceIntoArrays = function(arr, num) {
  //divides arr into num ~= arrays and returns them
  var ret = [];
  var div = parseInt(arr.length / num);
  var multiple = 1;
  while (multiple < num) {
    ret.push(arr.slice((multiple-1)*div, multiple*div))
    multiple += 1;
  }
  ret.push(arr.slice((multiple-1)*div));
  return ret;
}
