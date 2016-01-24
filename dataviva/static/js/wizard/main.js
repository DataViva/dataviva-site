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
        '$scope', '$http', "Wizard", "Question",
        function ($scope, $http, Wizard, Question) {

            $scope.start_session = function(session_name) {
                $scope.wizard = new Wizard(session_name);
            };

            $scope.select = function(q) {
                alert(q);
            };

            $scope.submit = function() {

                var data = {
                    "session_name": "locations",
                    "previous_answers": [["COM_INTERNACIONAL_STEP", true], ["EXPORTACOES_STEP", true]],
                    "current_answer": ["PRODUTO_STEP", true]
                };

                $http({
                    method: "POST",
                    url: "/en/wizard/submit_answer/",
                    data: data,
                })
                .success(function(resp){
                    $scope.wizard.current_step = resp.current_step;
                });
            };

        }]);


}());


fire_wizard = function(session_name) {
    $("#modal-wizard").modal();
    var el = document.getElementById('wizcont');
    angular.element(el).scope().start_session(session_name);
}
