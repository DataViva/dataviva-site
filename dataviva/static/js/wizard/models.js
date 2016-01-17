(function () {
    "use strict";

    var app = angular.module("wizard.models", [
        "wizard.remote",
    ]);

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

    app.service('Wizard', ["Remote", "$http", "$filter",  function (Remote, $http, $filter) {
        return function WizardStep(session_name) {
            var self = this;
            self.session_name = session_name;
            self.current_step = {
                "title": "Aguarde",
                "options": null,
            };

            $http({
                method: "GET",
                url: "/en/wizard/start_session/" + self.session_name,
            })
            .success(function(resp){
                self.current_step.title = resp.current_step.title;
                self.current_step.options = resp.current_step.options;
            })
            .error(function(resp){
                console.log(resp);
            })
        }
    }]);
}());
