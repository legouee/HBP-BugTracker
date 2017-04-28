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
    
    $scope.saveEditedTicket = function(pk){
      // get ticket form
      var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
      var title = $("#title").text()
      var text = $("#text").text()
      $.ajax({
         url:"",
         type:"POST",
         data: {'pk':JSON.stringify(pk) ,'title':title  ,'text':text, 'action':"edit_ticket", 'csrfmiddlewaretoken': csrftoken}, 

         success : function(json) {
            alert('Your ticket have been edited!' );
            },
         error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
            },
        });
      $("#ticket-title").replaceWith('<td id="ticket-title" class=title width=850>'+ title +'</td>');
      $("#ticket-text").replaceWith('<td id="ticket-text" class=text width=850>'+ text +'</td>');
      $("#TicketToEdit").hide();
      $("#TicketToShow").show();
      };
});

app.controller('CommentForm', function($scope) {
    $("#CommentToEdit").hide();
    // $scope.t=false
    $scope.editTicket = function(ticket){
      $("#TicketToEdit").show();
      $("#TicketToShow").hide();
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





  app.controller('Detail', function($scope) {
    // this is used to put the ctxstate in the URL of HBP
    $scope.init = function(pk)
    {
      $scope.pk = pk;
      sendState( $scope.pk);
    };
    
    var sendState = function(pk){
              window.parent.postMessage({
                  eventName: 'workspace.context',
                  
                  data: {
                      state: 'ticket.' + pk

                  }
              }, 'https://collab.humanbrainproject.eu/');
          };
  });

  app.controller('List', function($scope) {
  // this is used to clean the ctxstate in the URL of HBP when returning to list : no data
    var sendState = function(){
              window.parent.postMessage({
                  eventName: 'workspace.context',
                  data: {
                    state: 'ticket.n'
                  }
              }, 'https://collab.humanbrainproject.eu/');
          };
          sendState();
  });



}());