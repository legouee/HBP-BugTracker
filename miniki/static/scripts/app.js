(function() {
// Define the miniki application, currently doing nothing.
var app = angular.module('miniki', ['hbpCommon']);

app.controller('HomeForm', function($scope) {
   // The form controller that manage the displays of preview
   $scope.create = false
   $scope.createProject = function () {
     $scope.create = !$scope.create;
     console.log("create")
   };
});

// Bootstrap function
angular.bootstrap().invoke(function($http, $log) {
  $http.get('/config.json').then(function(res) {
    window.bbpConfig = res.data;
    angular.element(document).ready(function() {
      angular.bootstrap(document, ['miniki']);
    });
  }, function() {
    $log.error('Cannot boot miniki application');
  });
});

}());