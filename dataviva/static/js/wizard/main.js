(function () {
    "use strict";

    var app = angular.module('wizard', [
        "wizard.remote",
    ]);

    app.config(['$httpProvider', '$interpolateProvider',
        function ($httpProvider, $interpolateProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);

    app.controller('WizardController',[
        '$scope', "Remote",
        function ($scope, Remote) {

            console.log("Staring wiz controller");
            $scope.remote = new Remote();

            this.submit = function() {
                $scope.remote.submit();
            };

        }]);
}());
