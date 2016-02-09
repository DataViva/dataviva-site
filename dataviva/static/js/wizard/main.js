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
        '$scope', '$rootScope', '$templateRequest', '$compile', '$http', "Wizard",
        function ($scope, $rootScope, $templateRequest, $compile, $http, Wizard) {

            $rootScope.$on("Wizard.load_selector", function(ev, selector_url) {
                $(".selector-aerea").empty();
                $templateRequest(selector_url).then(function(html){
                    $scope.selector = true;d
                    var template = angular.element(html);
                    $(".selector-aerea").append(template);
                    $compile(template)($scope);
                });
            });

            $scope.start_session = function(session_name) {
                $scope.wizard = new Wizard(session_name);
            };

        }]);
    

    app.controller('LocationSelector',[
        '$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {

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

            $scope.select = function(id) {
                $rootScope.$broadcast('Selector.load_option', id);
            }; 

        }]);

        
        app.controller('ProductSelector',[
            '$scope', '$rootScope', '$http', function ($scope, $rootScope, $http) {

            $scope.section = {
                depth_factor: 2,
                filter_string: '',
                entries: []
            };

            $scope.position = {
                depth_factor: 6,
                filter_string: '',
                entries: []
            };

            $scope.load_depth_entries = function(group){
                if(group.entries.length > 0) return;

                $http({
                    method: "GET",
                    url: "/attrs/product?depth=" + group.depth_factor,
                })
                .success(function(resp){
                     group.entries = resp;
                });
            };

            $scope.select = function(id) {
                $rootScope.$broadcast('Selector.load_option', id);
            }; 

        }]);

}());


fire_wizard = function(session_name) {
    $("#modal-wizard").modal();
    var el = document.getElementById('wizcont');
    angular.element(el).scope().start_session(session_name);
}
