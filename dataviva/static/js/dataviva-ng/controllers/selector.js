(function () {
    "use strict";

    var app = angular.module('dataviva.controllers');

        app.controller('SelectorController',[
        '$scope', '$http', '$templateRequest', '$compile', 'Selectors',
        function ($scope, $http, $templateRequest, $compile, Selectors) {

            $scope.initialize = function(selector_name, selection_callback) {
                $scope.selector_model = new  Selectors[selector_name];
                $templateRequest($scope.selector_model.templateUrl).then(function(html){
                    var template = angular.element(html);
                    $(".selector-area").append(template);
                    $compile(template)($scope);
                    $('.nav-tabs li a')[0].click();
                });

            };
            
        }]);
}());