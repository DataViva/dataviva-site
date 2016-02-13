(function () {
    "use strict";

    var app = angular.module('dataviva.controllers');

    app.controller('WizardController',[
        '$scope', '$templateRequest', '$compile', '$http', 'Wizard', "Option", "Selectors", "$timeout",
        function ($scope, $templateRequest, $compile, $http, Wizard, Option, Selectors, $timeout) {

            $scope.start_session = function(session_name) {
                $scope.wizard = new Wizard(session_name);

                 $http({
                    method: "GET",
                    url: "/en/wizard/session/" + session_name,
                })
                .success(function(resp) {
                    $scope.new_step(resp);
                });
            };

            $scope.new_step = function(resp) {
                $scope.wizard.title = resp.title;
                if(resp.options) {                            
                    $scope.wizard.options = resp.options.map(function(val){
                        return new Option(val);
                    });
                } else {

                    $scope.selector_model = new Selectors.Location();
                    $templateRequest($scope.selector_model.templateUrl).then(function(html){
                        var template = angular.element(html);
                        $(".wiz-selector-area").append(template);
                        $compile(template)($scope);
                        $timeout(function(){
                             $('.nav-tabs button')[0].click();
                        }, 200);
                    });
                }
            };

            $scope.submit = function() {

                var post_params = {
                    "session_name": $scope.wizard.session_name,
                    "path_option": $scope.wizard.path_option,
                    "selectors": $scope.wizard.selectors,
                };

                $http.post("/en/wizard/submit_answer/", post_params)
                .success(function(resp){
                    $scope.new_step(resp.current_step);
                    $scope.wizard.selected_option = false;
                });

            };

    }]);

}());
