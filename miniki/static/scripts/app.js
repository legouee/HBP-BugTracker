(function() {

    // Define the miniki application, currently doing nothing.
    var app = angular.module('miniki', ['hbpCommon']);


    app.controller('TicketForm', function($scope) {
        // The form controller that manage the displays of preview
        $("#TicketToEdit").hide();
        // $scope.t=false
        $scope.editTicket = function(ticket) {
            $("#TicketToEdit").show();
            $("#TicketToShow").hide();
        };
    });

    app.controller('TicketEditSave', function($scope) {

        $scope.saveEditedTicket = function(pk) {
            // get ticket form
            var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
            var title = $("#title").text()
            var text = $("#text").text()
            $.ajax({
                url: "",
                type: "POST",
                data: { 'pk': JSON.stringify(pk), 'title': title, 'text': text, 'action': "edit_ticket", 'csrfmiddlewaretoken': csrftoken },

                success: function(json) {
                    alert('Your ticket havForme been edited!');
                },
                error: function(xhr, errmsg, err) {
                    console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                },
            });
            $("#ticket-title").replaceWith('<td id="ticket-title" class=title width=850>' + title + '</td>');
            $("#ticket-text").replaceWith('<td id="ticket-text" class=text width=850>' + text + '</td>');
            $("#TicketToEdit").hide();
            $("#TicketToShow").show();
        };
    });



    app.controller('CommentForm', function($scope) {

        $scope.editComment = function(pk) {
            var comtext = $("#editable-text-" + pk).text()
            angular.element(document.querySelector("#editable-text-" + pk)).attr('contenteditable', "true")
            _createButton("Save", saveEditedComment);

            function _createButton(name, func) {
                var btn = $('<input/>').attr({
                    'type': 'button',
                    'id': 'btn' + name,
                    'value': name
                }).bind('click', func);

                $("#panelForButtonSave-" + pk).append(btn);
            };

            function saveEditedComment() {
                // save in database
                var text = $("#editable-text-" + pk).text()
                var csrftoken = jQuery("[name=csrfmiddlewaretoken]").val();
                $.ajax({
                    url: "",
                    type: "POST",
                    data: { 'pk': JSON.stringify(pk), 'text': text, 'action': "edit_comment", 'csrfmiddlewaretoken': csrftoken },

                    success: function(json) {
                        alert('Your comment have been edited!');
                    },
                    error: function(xhr, errmsg, err) {
                        console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
                    },
                });
                //  change view
                $("#btnSave").remove();
                angular.element(document.querySelector("#editable-text-" + pk)).attr('contenteditable', "false")
            }
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
        $scope.init = function(pk) {
            $scope.pk = pk;
            sendState($scope.pk);
        };

        var sendState = function(pk) {
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
        var sendState = function() {
            window.parent.postMessage({
                eventName: 'workspace.context',
                data: {
                    state: 'ticket.n'
                },
            }, 'https://collab.humanbrainproject.eu/');
        };
        sendState();
    });


}());