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
                self.questions = [];
                self.selected_question = null;
                self.step = 0;

                self.path_option = null;
                self.selector_choices = [];

                self.select = function(question) {
                    self.selected_question = question;
                };

                self.start = function(session){
                    self.session_title = session.session_title;
                    self.title = session.title;
                    self.questions = session.questions.map(function(val){
                        return new Option(val);
                    });
                };

                self.load_selector = function(current_step, scope) {

                    var selectorProfile = Selector()
                            .callback(function(d){
                                self.selector_choices.push(d.id);
                                $('#modal-selector').modal('hide');
                                scope.submit();
                            });

                    function select_attr_profile(id) {
                          d3.select("#modal-selector-content").call(selectorProfile.type(id));
                          $('#modal-selector').modal('show');
                    }

                    select_attr_profile(dataviva.getUrlAttr(current_step));

                };
            };
    }]);

}());
