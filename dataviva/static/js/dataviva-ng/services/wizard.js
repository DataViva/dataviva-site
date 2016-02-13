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

    app.service('Wizard', ["$http", "Option",
        function ($http, Option) {
            
            return function Wizard(session_name) {
                var self = this;

                self.filter_string = ""
                self.session_name = session_name;
                self.session_title = "asdqwe11"
                self.options = [];

                self.path_option = null;
                self.selectors = [];

                self.select_path_option = function(option) {
                    self.path_option = option.id;
                    self.selected_option = option;
                };
            };
    }]);

}());
