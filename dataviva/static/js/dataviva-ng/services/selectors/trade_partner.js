(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('TradePartner',[
        '$http', function ($http) {

            var TradePartner = function(selection_callback) {
                var self = this;

                self.title = "Parceiros Comerciais do Brasil";

                self.templateUrl = "/en/wizard/trade_partner_selector/";
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
                            "/en/trade_partner/" +
                            hs_id
                        );
                    }
                }

                self.continents = {
                    depth_factor: 2,
                    filter_string: '',
                    entries: []
                };

                self.countries = {
                    depth_factor: 5,
                    filter_string: '',
                    entries: []
                };

                self.load_depth_entries = function(group){
                    if(!group || group.entries.length > 0) return;
                    self.loading = true;

                    $http({
                        method: "GET",
                        url: "/attrs/trade_partner?depth=" + group.depth_factor,
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
                self.load_depth_entries(self.continents);
            };

            return TradePartner;
    }]);
}());
