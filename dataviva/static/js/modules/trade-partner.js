$(document).ready(function(){
    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    var idIbge = $('#id_ibge').val();
    var idCountry = $('#id_country').val()
    var idContinent = $('#id_continent').val()
    var countryFilter, continentFilter, locationFilter;

    if (idCountry)
        countryFilter = 'country=' + idCountry;

    if (idContinent)
        continentFilter = 'continent=' + idContinent;

    if (idIbge != 'None')
        locationFilter = locations[idIbge.length] + '=' + idIbge;

    filter = [countryFilter, continentFilter, locationFilter].join('&');

    var isMunicipality = idIbge.length == 7;

    if(!isMunicipality) {
        BlueBox.add({
            url: dataviva.api_url + 'secex/year/municipality/?order=value&year=2017&direction=desc&limit=1&type=export&' + filter,
            title: dictionary['main_municipality'],
            subtitle: dictionary['by_value_exported'],
            preffix: 'USD ',
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'value',
            tab: 'international-trade'
        });

        BlueBox.add({
            url: dataviva.api_url + 'secex/year/municipality/?order=value&year=2017&direction=desc&limit=1&type=import&' + filter,
            title: dictionary['main_municipality'],
            subtitle: dictionary['by_value_imported'],
            preffix: 'USD ',
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'value',
            tab: 'international-trade'
        });

        General.add({
            url: dataviva.api_url + 'secex/year/municipality/?order=value&year=2017&direction=desc&limit=1&type=export&' + filter,
            title: dictionary['main_municipality_export'],
            preffix: 'USD ',
            label: {
                    metadata: true,
                    value: 'municipality'
                },
            value: 'value',
            id: 'partner',
        });

        General.add({
            url: dataviva.api_url + 'secex/year/municipality/?order=value&year=2017&direction=desc&limit=1&type=import&' + filter,
            title: dictionary['main_municipality_import'],
            preffix: 'USD ',
            label: {
                    metadata: true,
                    value: 'municipality'
                },
            value: 'value',
            id: 'partner',
        });
    }

    //BLUEBOXES ADD
    BlueBox.add({
        url: dataviva.api_url + 'secex/year/product/?order=value&year=2017&direction=desc&limit=1&type=export&' + filter,
        title: dictionary['main_product'],
        subtitle: dictionary['exported'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product'
        },
        value: 'value',
        tab: 'international-trade'
    });

    BlueBox.add({
        url: dataviva.api_url + 'secex/year/product/?order=value&year=2017&direction=desc&limit=1&type=import&' + filter,
        title: dictionary['main_product'],
        subtitle: dictionary['imported'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product'
        },
        value: 'value',
        tab: 'international-trade'
    });

    BlueBox.add({
        url: dataviva.api_url + 'secex/year/type/product/?year=2017&' + filter,
        title: dictionary['product_highest'],
        subtitle: dictionary['trade_balance'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product',
            funct: function(response, metadata) {
                var product = highestTradeBalance(response);
                return metadata[product.id].name_pt;
            }

        },
        value: function(response){
            var product = highestTradeBalance(response);
            return product.tradeBalance;
        },
        tab: 'international-trade'
    });

    BlueBox.add({
        url: dataviva.api_url + 'secex/year/type/product/?year=2017&' + filter,
        title: dictionary['product_lowest'],
        subtitle: dictionary['trade_balance'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product',
            funct: function(response, metadata) {
                var product = lowestTradeBalance(response);
                return metadata[product.id].name_pt;
            }

        },
        value: function(response){
            var product = lowestTradeBalance(response);
            return product.tradeBalance;
        },
        tab: 'international-trade'
    });


    //INDICATORS ADD
    Indicator.add({
        url: dataviva.api_url + "secex/year/type/?year=2017&" + filter,
        title: dictionary['trade_balance'] + ' (2017)',
        preffix: 'R$ ',
        value:  function (response) {
            var importValue = response.filter(function(item){return item.type == 'import'})[0].value;
            var exportValue = response.filter(function(item){return item.type == 'export'})[0].value;
            return exportValue - importValue;
        }
    });

    Indicator.add({
        url: dataviva.api_url + "secex/year/?year=2017&type=export&" + filter,
        title: dictionary['total_value_exported'] + ' (2017)',
        preffix: 'R$ ',
        value:  'value'
    });

    Indicator.add({
        url: dataviva.api_url + "secex/year/?year=2017&type=export&" + filter,
        title: dictionary['average_price_exported'] + ' (2017)',
        value:  function (response) {
            return (response[0].value / response[0].kg).toFixed(2);
        }
    });

    Indicator.add({
        url: dataviva.api_url + "secex/year/?year=2017&type=import&" + filter,
        title: dictionary['total_value_imported'] + ' (2017)',
        preffix: 'R$ ',
        value:  'value'
    });

    Indicator.add({
        url: dataviva.api_url + "secex/year/?year=2017&type=import&" + filter,
        title: dictionary['average_price_imported'] + ' (2017)',
        value:  function (response) {
            return (response[0].value / response[0].kg).toFixed(2);
        }
    });

    //GENERAL ADD 
    General.add({
        url: dataviva.api_url + 'secex/year/product/?order=value&year=2017&direction=desc&limit=1&type=export&' + filter,
        title: dictionary['main_product_export'],
        preffix: 'USD ',
        label: {
                metadata: true,
                value: 'product'
            },
        value: 'value',
        id: 'partner',
    });

    General.add({
        url: dataviva.api_url + 'secex/year/product/?order=value&year=2017&direction=desc&limit=1&type=import&' + filter,
        title: dictionary['main_product_import'],
        preffix: 'USD ',
        label: {
                metadata: true,
                value: 'product'
            },
        value: 'value',
        id: 'partner',
    });

    var highestTradeBalance = function(response){

        var products = {};

        response.forEach(function(item){
            if(!products[item.product]) {
                products[item.product] = {
                    export: 0,
                    import: 0
                };
            }
            products[item.product][item.type] = item.value;
        })

        var productId;
        var maxTradeBalance = 0;

        for(var key in products) {
            var tradeBalance = products[key].export - products[key].import;

            if(tradeBalance > maxTradeBalance){
                maxTradeBalance = tradeBalance;
                productId = key
            }
        }

        return {
            id: productId,
            tradeBalance: maxTradeBalance
        }
    }

    var lowestTradeBalance = function(response){

        var products = {};

        response.forEach(function(item){
            if(!products[item.product]) {
                products[item.product] = {
                    export: 0,
                    import: 0
                };
            }
            products[item.product][item.type] = item.value;
        })

        var productId;
        var minTradeBalance = 9999999999999999999;

        for(var key in products) {
            var tradeBalance = products[key].export - products[key].import;

            if(tradeBalance < minTradeBalance){
                minTradeBalance = tradeBalance;
                productId = key
            }
        }

        return {
            id: productId,
            tradeBalance: minTradeBalance
        }
    }

    General.add({
        url: dataviva.api_url + 'secex/year/type/product/?year=2017&' + filter,
        title: dictionary['product_highest_balance'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product',
            funct: function(response, metadata) {
                var product = highestTradeBalance(response);
                return metadata[product.id].name_pt;
            }

        },
        value: function(response){
            var product = highestTradeBalance(response);
            return product.tradeBalance;
        },
        id: 'partner',
    });

    General.add({
        url: dataviva.api_url + 'secex/year/type/product/?year=2017&' + filter,
        title: dictionary['product_lowest_balance'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'product',
            funct: function(response, metadata) {
                var product = lowestTradeBalance(response);
                return metadata[product.id].name_pt;
            }

        },
        value: function(response){
            var product = lowestTradeBalance(response);
            return product.tradeBalance;
        },
        id: 'partner',
    });
});