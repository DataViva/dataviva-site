(function () {
    "use strict";

    var app = angular.module('wizard', [
        "wizard.models",
    ]);

    app.config(['$httpProvider', '$interpolateProvider',
        function ($httpProvider, $interpolateProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);

    app.controller('WizardController',[
        '$scope', "Wizard", "WizardStep",
        function ($scope, Wizard, WizardStep) {

            console.log("Staring wiz controller");

            $scope.start_session = function(session_name) {
                alert("here!");
                $scope.wizard = new Wizard(session_name);
            };

            $scope.submit = function() {
                $scope.wizard.submit();
            };

        }]);
}());


fire_wizard = function(session_name) {
    $("#modal-wizard").modal();
    var el = document.getElementById('wizcont');
    angular.element(el).scope().start_session(session_name);
}
