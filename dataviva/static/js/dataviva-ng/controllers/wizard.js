(function () {
    "use strict";

    var app = angular.module('dataviva.controllers');

    app.controller('WizardController',[
        '$scope', '$http', 'Wizard',
        function ($scope, $http, Wizard) {

            $scope.start_session = function(session_name) {
                $scope.wizard = new Wizard(session_name);
                $scope.selector_model = null;


                 $http({
                    method: "GET",
                    url: "/en/wizard/session/" + session_name,
                })
                .success(function(resp) {
                    $scope.wizard.start(resp);
                });
            };
            

            $scope.submit = function() {

                $scope.wizard.step++;
                console.log($scope.wizard.step);

                if($scope.wizard.step > $scope.wizard.selected_question.selectors.length) {
                    // Redirect
                    var url = $scope.wizard.selected_question.redirect, 
                        i;

                    for(i in $scope.wizard.selector_choices) {
                        url = url.replace("%s", $scope.wizard.selector_choices[i])
                    }
                    window.location = url;
                } else {
                    $scope.wizard.load_selector($scope.wizard.selected_question.selectors[$scope.wizard.step - 1], $scope);
                    $('#modal-wizard').modal('hide');
                }

            };

    }]);

}());
