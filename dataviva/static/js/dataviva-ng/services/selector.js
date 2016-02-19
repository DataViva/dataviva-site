(function () {
    "use strict";

    var app = angular.module("dataviva.services.selectors");

    app.service('Selectors',[
            '$http', 'Location', 'Product', 'Industry', 'Major', 'BasicCourse', 'TradingPartner', 'University', 'Occupation',
                function ($http, Location, Product, Industry, Major, BasicCourse, TradingPartner, University, Occupation) {

                return {
                    BasicCourse: BasicCourse,
                    Industry: Industry,
                    Location: Location,
                    Major: Major,
                    Occupation: Occupation,
                    Product: Product,
                    TradingPartner: TradingPartner,
                    University: University,
                };
    }]);
}());
