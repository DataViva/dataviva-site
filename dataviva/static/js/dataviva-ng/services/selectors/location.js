(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Location',[
        '$http', function ($http) {

            var Location = function(selection_callback) {
                var self = this;

                self.title = "Localidades Brasileiras";

                self.templateUrl = "/en/wizard/location_selector/";
                self.selected_entry = null;

                /*
                    By default this selector redirects to the location page
                    But can be injected with a specfic callback
                */
                if(selection_callback) {
                    self.selection_callback = selection_callback;
                } else {
                    self.selection_callback = function(bra_id, event) {
                        window.location = (
                            window.location.protocol + 
                            "//" + 
                            window.location.host + 
                            "/en/location/" + 
                            bra_id
                        );
                    }
                }

                self.regions = {
                    depth_factor: 1,
                    filter_string: '',
                    entries: []
                };

                self.states = {
                    depth_factor: 3,
                    filter_string: '',
                    entries: []
                };

                self.mesoregions = {
                    depth_factor: 5,
                    filter_string: '',
                    entries: []
                };

                self.mircroregions = {
                    depth_factor: 7,
                    filter_string: '',
                    entries: []
                };

                self.municipalities = {
                    depth_factor: 9,
                    filter_string: '',
                    entries: [],
                };

                self.load_depth_entries = function(group){
                    if(!group || group.entries.length > 0) return;
                    self.loading = true;
                    $http({
                        method: "GET",
                        url: "/attrs/location?depth=" + group.depth_factor,
                    })
                    .then(function(resp){
                        group.entries = resp.data;
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

                self.load_depth_entries(self.regions);

                self.toString = function() {
                    return 'bra';
                }
            };

            return Location;
    }]);
}());
