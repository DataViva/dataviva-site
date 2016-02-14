(function () {
    "use strict";

    var app = angular.module("dataviva.services");

    app.service('Option', [ function () {
        return function Option(args) {

            var self = this;
            var defaults = {
                selected: false,
            };
            angular.extend(this, defaults, args);
        }
    }]);

    app.service('Wizard', ["Option", "Selectors", "$templateRequest", "$compile", "$timeout",
        function (Option, Selectors, $templateRequest, $compile, $timeout) {
            
            return function Wizard(session_name) {
                var self = this;

                self.filter_string = ""
                self.session_name = session_name;
                self.options = [];

                self.path_option = null;
                self.selector_choices = [];

                self.select = function(option) {
                    self.selected_option = option.id;
                };

                self.new_step = function(current_step, scope) {
                    self.title = current_step.title;
                    self.step_type = null;

                    if(current_step.options) {
                        self.step_type = "path_option";
                        self.options = current_step.options.map(function(val){
                            return new Option(val);
                        });

                    } else {
                        self.step_type = "selector";
                        scope.selector_model = new Selectors[current_step.type](function(id) {
                            self.selected_option = id;
                        });

                        $templateRequest(scope.selector_model.templateUrl).then(function(html){
                            var template = angular.element(html);
                            $(".wiz-selector-area").empty();
                            $(".wiz-selector-area").append(template);
                            $compile(template)(scope);
                            $timeout(function(){$('.nav-tabs li a')[0].click()}, 500);
                        });
                    }
                };
            };
    }]);

}());
