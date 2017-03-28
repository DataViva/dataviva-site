var map = document.getElementById('map'),
    dataset = map.getAttribute('dataset'),
    value = map.getAttribute('value'),
    lang = 'pt';
    apiFilters = map.getAttribute('filters');

var args = getUrlArgs(),
    filters = args['filters'] ? args['filters'].split('+') : FILTERS[dataset]['state'] || [];

var buildData = function(apiResponse,statesMetadata, otherMetadata) {

    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    };

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header) {
                dataItem[header] = getAttrByName(item, header);
            });

            dataItem['id'] = statesMetadata[dataItem['state']]['abbr_' + lang];
            dataItem['stateName'] = statesMetadata[dataItem['state']]['name_' + lang];
            filters.forEach(function(filter){
                try{
                for (d in otherMetadata)
                   dataItem[d] = otherMetadata[d][dataItem[d]]['name_' + lang];

                }catch(e){
                } 
            });
            data.push(dataItem);
            
        } catch(e) {

        };
    });
    return data;
}

var loadViz = function(data){
    var uiBuilder = function() {
        var ui = [];
        var statements = function(filter, value){

            return data.filter(function(item) {
                return  item[filter] == value});
        };
        // Adds filters selector
        filters.forEach(function(filter) {
            var options = [];
            var key = -1;
            var values = {};
            var label = dictionary['all'];
            values[label] = label
            options.push(values);
            for (id in otherMetadata[filter]) {
                            key = otherMetadata[filter][id].id;
                            values = {};
                            label = otherMetadata[filter][id]['name_' + lang];
                            values[label] = label;
                           options.push(values)
                       }

            ui.push({
                'method': function(value) {
                    viz.data(statements(filter, value));
                    viz.draw();
                
                },
                'type': 'drop',
                'label': dictionary[filter],
                'value': options,
            });
        });

        return ui;
    };

    var viz = d3plus.viz()
        .container('#map')
        .data(data)
        .type('geo_map')
        .coords({'value': '/pt/map/coords'})
        .format(formatHelper())
        .tooltip({'sub': 'stateName'})
        .ui(uiBuilder())
        .id('id')
        .time('year')
        .color({'heatmap': ["#282F6B", "#B22200"],
                'value': value})
        .draw()
}


var getUrls = function() {
    var dimensions = [dataset, 'year', 'state'];
    var metadata = [];
    
    filters.forEach(function(attr) {
        if (attr != 'state' && dimensions.indexOf(attr) == -1) {
            dimensions.push(attr);
            metadata.push(attr);
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + apiFilters,
        API_DOMAIN + '/metadata/' + 'state'
    ];

    if (dataset.match(/^cnes_/)) {
        metadata.forEach(function(attr) {
            urls.push(API_DOMAIN + '/metadata/' + attr)
        });
    }

    return urls;
};


$(document).ready(function() {
         ajaxQueue(
    //     ['http://api.staging.dataviva.info/'+dataset +'/year/state?'+filters, 'http://api.staging.dataviva.info/metadata/state'], 
        getUrls(),
        function(responses) {
            var data = responses[0];
            statesMetadata = responses[1],
            otherMetadata = {};

            if (dataset.match(/^cnes_/)){
                filters.forEach(function(depth, i) {
                    otherMetadata[depth] = responses[2+i];
                });
            }

            data = buildData(data,statesMetadata,otherMetadata);
            loadViz(data);


            // loading.hide();
            d3.select('#mask').remove();
        }
    );
});
