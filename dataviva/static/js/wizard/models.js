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

    app.service('Wizard', ["Remote", "$filter",  function (Remote, $filter) {
        return function WizardStep(session_name) {
            alert("TODO fetch wiz/flow from server for: " + session_name);
        }
    }]);
}());
