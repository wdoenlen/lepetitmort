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
