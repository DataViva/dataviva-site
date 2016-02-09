(function () {
    "use strict";

    var app = angular.module("wizard.models", []);

    app.service('Option', [ function () {
        return function Option(args) {

            var self = this;
            var defaults = {
                selected: false,
            };
            angular.extend(this, defaults, args);
        }
    }]);

    app.service('Wizard', ["$http", '$rootScope', "Option",
        function ($http, $rootScope, Option) {
            
            return function Wizard(session_name) {
                var self = this;

                self.filter_string = ""
                self.session_name = session_name;
                self.session_title = "asdqwe11"
                self.options = [];

                self.path_option = null;
                self.selectors = [];

                self.new_step = function(resp) {
                    self.title = resp.title;
                    if(resp.options) {                            
                        self.options = resp.options.map(function(val){
                            return new Option(val);
                        });

                    } else {
                        $rootScope.$broadcast('Wizard.load_selector', resp.selector_url);
                    }
                };

                self.start_session = function(){
                    $http({
                        method: "GET",
                        url: "/en/wizard/session/" + self.session_name,
                    })
                    .success(function(resp) {
                        self.new_step(resp);                        
                    });
                };


                self.select_path_option = function(option) {
                    self.path_option = option.id;
                    self.selected_option = option;
                };

                $rootScope.$on("Selector.load_option", function(ev, id){
                    self.selectors.push(id);
                    self.selected_option = id;
                });

                self.submit = function() {

                    var post_params = {
                        "session_name": self.session_name,
                        "path_option": self.path_option,
                        "selectors": self.selectors,
                    };

                    $http.post("/en/wizard/submit_answer/", post_params)
                    .success(function(resp){
                        self.new_step(resp.current_step);
                        self.selected_option = false;
                    });

                };

                self.start_session();
            };
    }]);
}());
