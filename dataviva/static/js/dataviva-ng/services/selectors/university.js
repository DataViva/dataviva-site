(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('University',[
        '$http', function ($http) {

            var University = function(selection_callback) {
                var self = this;

                self.title = "Universidades";

                self.templateUrl = "/en/wizard/university_selector/";
                self.selected_entry = null;
                self.selection_callback = selection_callback;

                /*
                    By default this selector redirects to the location page
                    But can be injected with a specfic callback
                */
                if(selection_callback) {
                    self.selection_callback = selection_callback;
                } else {
                    self.selection_callback = function(id, event) {
                        window.location = (
                            window.location.protocol +
                            "//" +
                            window.location.host +
                            "/en/university/" +
                            id
                        );
                    }
                }

                self.universities = {
                    depth_factor: 5,
                    filter_string: '',
                    entries: []
                };

                self.load_depth_entries = function(group){
                    if(!group || group.entries.length > 0) return;
                    self.loading = true;

                    $http({
                        method: "GET",
                        url: "/attrs/university?depth=" + group.depth_factor,
                    })
                    .then(function(resp){
                        group.entries = resp.data.data;
                        self.loading = false;
                    }, function(errorResp){
                        self.loading = false;
                        self.error = "Sorry. An error has occurred while loading the options.";
                    });
                };

                self.select = function(id, event) {
                    self.selected_entry = id;
                    self.selection_callback(id, event);
                };

                // NOTE: NECESSARY TO LOAD THE FIRST TAB CONTENT UPFRONT
                self.load_depth_entries(self.universities);
            };

            return University;
    }]);
}());
