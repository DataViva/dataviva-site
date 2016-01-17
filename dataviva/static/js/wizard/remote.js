(function () {
    "use strict";

    var app = angular.module("wizard.remote", []);

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
