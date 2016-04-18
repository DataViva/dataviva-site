(function () {
    "use strict";

    var app = angular.module('dataviva.controllers');

        app.controller('SelectorController',[
        '$scope', '$http', '$templateRequest', '$compile', 'Selectors', '$timeout',
        function ($scope, $http, $templateRequest, $compile, Selectors, $timeout) {

            $scope.initialize = function(selector_name, selection_callback) {
                $scope.selector_model = new Selectors[selector_name](selection_callback);

                $templateRequest($scope.selector_model.templateUrl).then(function(html){
                    var template = angular.element(html);
                    $(".selector-area").append(template);
                    $timeout(function(){
                        $compile(template)($scope);

                        // Some selectors might have no tabs (e.g: University)
                        // so we should check
                        var firstTab = $('.nav-tabs li a')[0];
                        if(typeof(firstTab) != "undefined") {
                            firstTab.click();
                        }

                    }, 300);
                }, function(errorResp) {
                    $scope.selector_model.error = "Sorry, a error has occurred.";
                });

            };

        }]);
}());