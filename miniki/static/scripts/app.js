(function() {
// Define the miniki application, currently doing nothing.
var app = angular.module('miniki', ['hbpCommon']);


app.controller('TicketForm', function($scope) {
   // The form controller that manage the displays of preview
    $("#TicketToEdit").hide();
    // $scope.t=false
    $scope.editTicket = function(ticket){
      $("#TicketToEdit").show();
      $("#TicketToShow").hide();
    };
});

app.controller('TicketEditSave', function($scope) {
    $scope.saveEditedTicket = function(){
      // get ticket form
      $.ajax({
        url:"",
        type:"POST",
        data: {title: $("#title").text() ,text:$("#text").text() }, 

       success : function(json) {
            console.log(json); // another sanity check
            //On success show the data posted to server as a message
            alert('Hi ' );
       },
      error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
      }
      });

      $("#TicketToEdit").hide();
      $("#TicketToShow").show();
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