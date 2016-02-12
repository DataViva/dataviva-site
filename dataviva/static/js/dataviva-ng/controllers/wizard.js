(function () {
    "use strict";

    var app = angular.module('dataviva.controllers', [
        'dataviva.services'
    ]);

    app.controller('WizardController',[
        '$scope', '$rootScope', '$templateRequest', '$compile', '$http', 'Wizard',
        function ($scope, $rootScope, $templateRequest, $compile, $http, Wizard) {

            $scope.load_selector = function(ev, selector_url) {

                $(".selector-area").empty();

                $templateRequest(selector_url).then(function(html){
                    $scope.selector = true;
                    var template = angular.element(html);
                    $(".selector-aerea").append(template);
                    $compile(template)($scope);
                });
            };

            $rootScope.$on("Wizard.load_selector", $scope.load_selector);

            $scope.start_session = function(session_name) {
                $scope.wizard = new Wizard(session_name);
            };
    }]);

}());
