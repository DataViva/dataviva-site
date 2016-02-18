(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Selectors',[
            '$http', 'Location', 'Product', 'Industry', 'Major', 'BasicCourse',
                function ($http, Location, Product, Industry, Major, BasicCourse) {
                return {
                    BasicCourse: BasicCourse,
                    Industry: Industry,
                    Location: Location,
                    Major: Major,
                    Product: Product,
                };
    }]);
}());

