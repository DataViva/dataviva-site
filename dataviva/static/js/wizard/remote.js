(function () {
    "use strict";

    var app = angular.module("wizard.remote", []);

    app.service('WizardStep', ["$filter",  function ($filter) {
        return function WizardStep(args) {

            var self = this;
            var defaults = {
                title: null,
                results: [],
            };
            angular.extend(this, defaults, args);
            alert("initialized wizard step");
        }
    }]);

    app.service('Remote', ["$http", "WizardStep",

        function ($http, WizardStep, Result) {

            return function Remote(args) {

                this.submit = function() {

                    $http({
                        method: 'POST',
                        url: "/wizard/submit",
                    })
                    .success(function(resp){
                        alert("submit success");
                    });

                }; // END SUBMIT FUNCTION
            }
    }]);
}());
