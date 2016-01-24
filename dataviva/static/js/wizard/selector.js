(function () {
    "use strict";

    var app = angular.module('selector', [
        //"selector.models",
    ]);

    app.config(['$httpProvider', '$interpolateProvider',
        function ($httpProvider, $interpolateProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);

    app.controller('LocationSelector',[
        '$scope', '$http',
        function ($scope, $http) {

            $scope.regions = {
                depth_factor: 1,
                filter_string: '',
                entries: []
            };

            $scope.states = {
                depth_factor: 3,
                filter_string: '',
                entries: []
            };

            $scope.mesoregions = {
                depth_factor: 5,
                filter_string: '',
                entries: []
            };

            $scope.mircroregions = {
                depth_factor: 7,
                filter_string: '',
                entries: []
            };

            $scope.municipalities = {
                depth_factor: 9,
                filter_string: '',
                entries: [],
            };

            $scope.filter = function(group){
                if(group.filter_string.length > 2) {
                    console.log("x: " + group.filter_string);
                } else {
                    group.filtered_entries = group.entries;
                }
            };

            $scope.load_depth_entries = function(group){
                if(group.entries.length > 0) return;

                $http({
                    method: "GET",
                    url: "/attrs/location?depth=" + group.depth_factor,
                })
                .success(function(resp){
                     group.entries = resp;
                });
            };

        }]);


}());