(function () {
    "use strict";

    var app = angular.module("dataviva.services");

    app.service('Selectors',[
            '$http', function ($http) {

                var Location = function(selection_callback) {
                    var self = this;
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
                        .success(function(resp){
                            group.entries = resp;
                            self.loading = false;
                        });
                    };

                    self.select = function(id, event) {
                        self.selected_entry = id;
                        self.selection_callback(id, event);
                    };

                    self.load_depth_entries(self.regions);
                };

                var Product = function(selection_callback) {
                    var self = this;
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
                    self.load_depth_entries(self.sections);
                };

                var BasicCourse = function(selection_callback) {
                    var self = this;
                    self.templateUrl = "/en/wizard/basic_course_selector/";
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
                                "/en/basic_course/" + 
                                hs_id
                            );
                        }
                    }

                    self.fields = {
                        depth_factor: 2,
                        filter_string: '',
                        entries: []
                    };

                    self.courses = {
                        depth_factor: 5,
                        filter_string: '',
                        entries: []
                    };

                    self.load_depth_entries = function(group){
                        if(!group || group.entries.length > 0) return;
                        self.loading = true;

                        $http({
                            method: "GET",
                            url: "/attrs/basic_course?depth=" + group.depth_factor,
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
                    self.load_depth_entries(self.fields);
                };

                return {
                    Location: Location,
                    Product: Product,
                    BasicCourse: BasicCourse,
                };
    }]);
}());
