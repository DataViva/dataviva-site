(function () {
    "use strict";

    var app = angular.module('dataviva.controllers', ['dataviva.services']);

        app.controller('SelectorController',[
        '$scope', '$http', '$templateRequest', '$compile', 'Selectors',
        function ($scope, $http, $templateRequest, $compile, Selectors) {

            $scope.selectors = {
                location: {
                    templateUrl: '/en/wizard/location_selector/',
                    model: Selectors.Location,
                },
                product: {
                    templateUrl: '/en/wizard/product_selector/',
                    model: Selectors.Product,
                },
            };

            $scope.initialize = function(selector_name, selection_callback) {

                var selector = $scope.selectors[selector_name];

                $templateRequest(selector.templateUrl).then(function(html){
                    var template = angular.element(html);
                    $(".selector-area").append(template);
                    $compile(template)($scope);
                });

                $scope.model = new selector.model(selection_callback);
            };
            
        }]);
}());