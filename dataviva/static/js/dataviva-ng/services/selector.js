(function () {
    "use strict";

    var app = angular.module("dataviva.services", []);

    app.service('Selectors',[
            '$http', function ($http) {

                var Location = function(selection_callback) {
                    var self = this;
                    self.selected_entry = null;
                    self.selection_callback = selection_callback;

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

                        $http({
                            method: "GET",
                            url: "/attrs/location?depth=" + group.depth_factor,
                        })
                        .success(function(resp){
                             group.entries = resp;
                        });
                    };

                    self.select = function(id) {
                        self.selected_entry = id;
                        self.selection_callback(id);
                    };

                    self.load_depth_entries(self.regions);
                };

                var Product = function(selection_callback) {
                    var self = this;
                    self.selected_entry = null;
                    self.selection_callback = selection_callback;

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

                        $http({
                            method: "GET",
                            url: "/attrs/product?depth=" + group.depth_factor,
                        })
                        .success(function(resp){
                             group.entries = resp;
                        });
                    };

                    self.select = function(id) {
                        self.selected_entry = id;
                        self.selection_callback(id);
                    };

                    // NOTE: NECESSARY TO LOAD THE FIRST TAB CONTENT UPFRONT
                    self.load_depth_entries(self.sections);
                };

                return {
                    Location: Location,
                    Product: Product,
                };
    }]);
}());
