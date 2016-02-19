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
                    $scope.wizard.new_step(resp);
                });
            };
            

            $scope.submit = function() {

                if($scope.wizard.step_type == "selector") {
                    $scope.wizard.selector_choices.push($scope.wizard.selected_option);
                } else {
                    $scope.wizard.path_option = $scope.wizard.selected_option;
                }

                var post_params = {
                    "session_name": $scope.wizard.session_name,
                    "path_option": $scope.wizard.path_option,
                    "selector_choices": $scope.wizard.selector_choices,
                };

                $http.post("/en/wizard/submit_answer/", post_params)
                .success(function(resp){
                    if (resp.redirect_url) {
                        window.location = resp.redirect_url;
                        return;
                    } else {
                        $scope.wizard.new_step(resp.current_step, $scope);
                        $scope.wizard.selected_option = false;
                    }
                });

            };

    }]);

}());
