(function() {
// Define the miniki application, currently doing nothing.
angular.module('miniki', ['hbpCommon'])
.controller('TicketPageForm', function($scope) {
  
  // The form controller that manage the displays of preview.
  $scope.isPreviewOpen = false;
  $scope.togglePreview = function () {
    $scope.isPreviewOpen = !$scope.isPreviewOpen;
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