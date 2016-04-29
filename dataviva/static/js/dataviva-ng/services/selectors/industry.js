(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Industry',[
        '$http', function ($http) {

            var Industry = function(selection_callback) {
                var self = this;

                self.title = "Atividades Econômicas";

                self.templateUrl = "/en/wizard/industry_selector/";
                self.selected_entry = null;
                self.selection_callback = selection_callback;

                /*
                    By default this selector redirects to the location page
                    But can be injected with a specfic callback
                */
                if(selection_callback) {
                    self.selection_callback = selection_callback;
                } else {
                    self.selection_callback = function(cnae_id, event) {
                        window.location = (
                            window.location.protocol + 
                            "//" + 
                            window.location.host + 
                            "/en/industry/" + 
                            cnae_id
                        );
                    }
                }

                self.classes = {
                    depth_factor: 1,
                    filter_string: '',
                    entries: []
                };

                self.divisions = {
                    depth_factor: 3,
                    filter_string: '',
                    entries: []
                };

                self.sections = {
                    depth_factor: 6,
                    filter_string: '',
                    entries: []
                };

                self.load_depth_entries = function(group){
                    if(!group || group.entries.length > 0) return;
                    self.loading = true;

                    $http({
                        method: "GET",
                        url: "/attrs/industry?depth=" + group.depth_factor,
                    })
                    .success(function(resp){
                         group.entries = resp;
                         self.loading = false;
                    });
                };

                self.select = function(id, event) {
                    self.selected_entry = id;
                    self.selection_callback(id, event);
                };

                // NOTE: NECESSARY TO LOAD THE FIRST TAB CONTENT UPFRONT
                self.load_depth_entries(self.classes);
            };

            return Industry;
    }]);
}());
