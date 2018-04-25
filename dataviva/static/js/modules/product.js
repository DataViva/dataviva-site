$(document).ready(function(){
    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    var product = location.pathname.split('/')[3];
    var productFilter = '';
    var productDepth = 'product';

    if (product.length == 2){
        productFilter = 'product_section=' + product;
        productDepth = 'product_section';
    }
    if (product.length == 6)
        productFilter = 'product=' + product.slice(2, 6)

    var idIbge = $('#id_ibge').val();
    var locationFilter = ''
    if (idIbge != 'None')
        locationFilter = idIbge ? locations[idIbge.length] + '=' + idIbge : '';

    filter = [productFilter, locationFilter].join('&');
    var isMunicipality = idIbge.length == 7;


    if(!isMunicipality) {
        BlueBox.add({
            url: 'http://api.staging.dataviva.info/secex/year/municipality/?order=value&year=2016&direction=desc&limit=1&type=export&' + filter,
            title: dictionary['main_municipality'],
            subtitle: dictionary['by_value_exported'],
            preffix: 'USD ',
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'value',
            tab: 'trade-partner'
        });

        BlueBox.add({
            url: 'http://api.staging.dataviva.info/secex/year/municipality/?order=value&year=2016&direction=desc&limit=1&type=import&' + filter,
            title: dictionary['main_municipality'],
            subtitle: dictionary['by_value_imported'],
            preffix: 'USD ',
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'value',
            tab: 'trade-partner'
        });

        General.add({
            url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/year/municipality/?order=value&year=2016&direction=desc&limit=1&type=export&' + filter,
            title: dictionary['main_municipality_export'],
            preffix: 'USD ',
            label: {
                    metadata: true,
                    value: 'municipality',
                    funct: function(response, metadata) {
                        debugger
                        var id = response[0].municipality;
                        return metadata[id].name_pt + ' - ' + metadata[id].state.abbr_pt;
                    }
                },
            value: 'value',
            id: 'product',
        });

        General.add({
            url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/year/municipality/?order=value&year=2016&direction=desc&limit=1&type=import&' + filter,
            title: dictionary['main_municipality_import'],
            preffix: 'USD ',
            label: {
                    metadata: true,
                    value: 'municipality',
                    funct: function(response, metadata) {
                        debugger
                        var id = response[0].municipality;
                        return metadata[id].name_pt + ' - ' + metadata[id].state.abbr_pt;
                    }
                },
            value: 'value',
            id: 'product',
        });
    }

    //BLUEBOXES ADD
    BlueBox.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/country/year/?order=value&year=2016&direction=desc&limit=1&type=export&' + filter,
        title: dictionary['main_destination'],
        subtitle: dictionary['by_value_exported'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'country'
        },
        value: 'value',
        tab: 'trade-partner'
    });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/country/year/?order=value&year=2016&direction=desc&limit=1&type=import&' + filter,
        title: dictionary['main_origin'],
        subtitle: dictionary['by_value_imported'],
        preffix: 'USD ',
        label: {
            metadata: true,
            value: 'country'
        },
        value: 'value',
        tab: 'trade-partner'
    });


    //INDICATORS ADD

    Indicator.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/type/?year=2016&' + filter,
        title: dictionary['trade_balance'] + ' (2016)',
        preffix: 'R$ ',
        value:  function (response) {
            var importValue = response.filter(function(item){return item.type == 'import'})[0];
            var exportValue = response.filter(function(item){return item.type == 'export'})[0];

            importValue = importValue == undefined ? 0 : importValue.value;
            exportValue = exportValue == undefined ? 0 : exportValue.value;

            return exportValue - importValue;
        }
    });

    Indicator.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/year?year=2016&type=export&' + filter,
        title: dictionary['total_value_exported'] + ' (2016)',
        preffix: 'R$ ',
        value:  'value'
    });

    Indicator.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/?year=2016&type=export&' + filter,
        title: dictionary['average_price_exported'] + ' (2016)',
        suffix: 'USD / kg',
        value:  function (response) {
            return (response[0].value / response[0].kg).toFixed(2);
        }
    });

    Indicator.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/year?year=2016&type=import&' + filter,
        title: dictionary['total_value_imported'] + ' (2016)',
        preffix: 'R$ ',
        value:  'value'
    });

    Indicator.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/year/?year=2016&type=import&' + filter,
        title: dictionary['average_price_imported'] + ' (2016)',
        suffix: 'USD / kg',
        value:  function (response) {
            return (response[0].value / response[0].kg).toFixed(2);
        }
    });

    //GENERAL ADD 
    General.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/country/year/?order=value&year=2016&direction=desc&limit=1&type=export&' + filter,
        title: dictionary['main_destination_exported'],
        preffix: 'USD ',
        label: {
                metadata: true,
                value: 'country'
            },
        value: 'value',
        id: 'product',
    });

    General.add({
        url: 'http://api.staging.dataviva.info/secex/' + productDepth + '/country/year/?order=value&year=2016&direction=desc&limit=1&type=import&' + filter,
        title: dictionary['main_origin_imported'],
        preffix: 'USD ',
        label: {
                metadata: true,
                value: 'country'
            },
        value: 'value',
        id: 'product',
    });
});
