(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Product',[
        '$http', function ($http) {

            var Product = function(selection_callback) {
                var self = this;

                self.title = "Produtos";

                self.templateUrl = "/en/wizard/product_selector/";
                self.selected_entry = null;
                self.selection_callback = selection_callback;

                /*
                    By default this selector redirects to the location page
                    But can be injected with a specfic callback
                */
                if(selection_callback) {
                    self.selection_callback = selection_callback;
                } else {
                    self.selection_callback = function(hs_id, event) {
                        window.location = (
                            window.location.protocol + 
                            "//" + 
                            window.location.host + 
                            "/en/product/" + 
                            hs_id
                        );
                    }
                }

                self.sections = {
                    depth_factor: 2,
                    filter_string: '',
                    entries: []
                };

                self.positions = {
                    depth_factor: 6,
                    filter_string: '',
                    entries: []
                };

                self.load_depth_entries = function(group){
                    if(!group || group.entries.length > 0) return;
                    self.loading = true;

                    $http({
                        method: "GET",
                        url: "/attrs/product?depth=" + group.depth_factor,
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

                // NOTE: NECESSARY TO LOAD THE FIRST TAB CONTENT UPFRONT
                self.load_depth_entries(self.sections);
            };

            return Product;
    }]);
}());
