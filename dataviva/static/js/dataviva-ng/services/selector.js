(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Selectors',[
            '$http', 'Location', 'Product', 'Industry', 'Major', 'BasicCourse', 'TradePartner', 'University', 'Occupation',
                function ($http, Location, Product, Industry, Major, BasicCourse, TradePartner, University, Occupation) {

                return {
                    BasicCourse: BasicCourse,
                    Industry: Industry,
                    Location: Location,
                    Major: Major,
                    Occupation: Occupation,
                    Product: Product,
                    TradePartner: TradePartner,
                    University: University,
                };
    }]);
}());
