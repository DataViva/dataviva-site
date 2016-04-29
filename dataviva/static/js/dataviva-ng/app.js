(function () {
    "use strict";

    var app = angular.module('dataviva', [
        "dataviva.services",
        "dataviva.services.selectors",
        "dataviva.controllers",
    ]);

    app.config(['$httpProvider', '$interpolateProvider',
        function ($httpProvider, $interpolateProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
        $interpolateProvider.startSymbol('{$');
        $interpolateProvider.endSymbol('$}');
    }]);

}());


fire_wizard = function(session_name) {
    $("#modal-wizard").modal();    
    $(".wiz-selector-area").empty();
    var el = document.getElementById('wizcont');
    angular.element(el).scope().start_session(session_name);
};

start_selector = function(selector_name, selection_callback) {
    $("#modal-selector").modal();
    var el = document.getElementById('selectorCont');
    $(".selector-area").empty();
    angular.element(el).scope().initialize(selector_name, selection_callback);
};
