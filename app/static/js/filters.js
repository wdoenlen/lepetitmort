/* Filters */
round = function(input, precision) {
  return input ?
    parseFloat(input).toFixed(precision) :
    "";
}

angular.module('deathmsgFilters', [])
  .filter('prettifyDate', function() {
    return function(date) {
      return new Date(date).toDateString('yyyy-MM-dd');
    }
  })
  .filter('uppercase', function() {
    return function(input) {
      return input.toUpperCase();
    }
  })
  .filter('title', function() {
    return function(input) {
      if (!input) {
        return '';
      }
      return input.split(' ').map(function(x) {return x[0].toUpperCase() + x.slice(1)}).join(' ')
    }
  });