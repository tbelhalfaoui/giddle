angular.module('GiddleApp.directives', [])
  .directive('setFocus', function() {
    return {
      scope: {
        setFocus: '='
      },
      restrict: 'A',
      link : function($scope, $elem) {
        $scope.$watch('setFocus', function(condition) {
          if (condition) {
            $elem[0].focus();
          }
        });
      }
    }
  });

