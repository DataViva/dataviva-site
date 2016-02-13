(function () {
    "use strict";

    var app = angular.module('dataviva.controllers');

        app.controller('SelectorController',[
        '$scope', '$http', '$templateRequest', '$compile', 'Selectors',
        function ($scope, $http, $templateRequest, $compile, Selectors) {

            $scope.selectors = {
                location: {
                    model: Selectors.Location,
                },
                product: {
                    model: Selectors.Product,
                },
            };

            $scope.initialize = function(selector_name, selection_callback) {

                var selector = $scope.selectors[selector_name];
                $scope.selector_model = new selector.model(selection_callback);

                $templateRequest($scope.selector_model.templateUrl).then(function(html){
                    var template = angular.element(html);
                    $(".selector-area").append(template);
                    $compile(template)($scope);
                    $('.nav-tabs button')[0].click();
                });

            };
            
        }]);
}());