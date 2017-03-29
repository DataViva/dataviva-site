var map = document.getElementById('map'),
    dataset = map.getAttribute('dataset'),
    value = map.getAttribute('value'),
    apiFilters = map.getAttribute('filters'),
    validOccupations = {},
    currentFilters = {};

var args = getUrlArgs(),
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    values = args.hasOwnProperty('values') ? args['values'].split('+') : SIZES[dataset]['state'] || [value];

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

            if (dataItem.hasOwnProperty('occupation_family'))
                validOccupations[dataItem['occupation_family']] = 1;

            dataItem['id'] = statesMetadata[dataItem['state']]['abbr_' + lang];
            dataItem['stateName'] = statesMetadata[dataItem['state']]['name_' + lang];

            for (d in otherMetadata)
                dataItem[d] = otherMetadata[d][dataItem[d]]['name_' + lang];

            data.push(dataItem);
    
        } catch(e) {

        };
    });
    return data;
}

var loadViz = function(data){
    var uiBuilder = function() {
        var ui = [];

        var filteredData = function() {
            return data.filter(function(item) {
                var valid = true,
                    keys = Object.keys(currentFilters);

                for (var i = 0; i < keys.length; i++) {
                    if (currentFilters[keys[i]] == -1)
                        continue;
                    if (item[keys[i]] != currentFilters[keys[i]]) {
                        valid = false;
                        break;
                    }
                }

                return valid;
            });
        };

        // Adds size selector
        if (values.length > 1) {
            var options = [];
            values.forEach(function(item) {
                options.push({[dictionary[item]]: item});
            });

            ui.push({
                'method': function(value) {
                    var d = filteredData();
                    d.forEach(function(item) {
                        if (item[value] == 0)
                            item[value] = null;
                    });
                    viz.data(d);
                    viz.color(value);
                    viz.draw();
                },
                'type': options.length > 3 ? 'drop' : '',
                'label': dictionary['value'],
                'value' : options
            });
        }

        var statements = function(filter, value){
            if(dictionary['all'] == value)
                return data

            return data.filter(function(item) {
                return  item[filter] == value});
        };

        // Adds filters selector
        filters.forEach(function(filter, j) {
            currentFilters[filter] = -1;
            var options = [];
            if (!j) {
                for (id in otherMetadata[filter]) {
                    if (filter == 'occupation_family' && !validOccupations.hasOwnProperty(id))
                        continue;
                    var label = otherMetadata[filter][id]['name_' + lang],
                        option = {};
                    option[label] = label;
                    options.push(option);
                }

                options.sort(function(a, b) {
                    if (Object.keys(a)[0] < Object.keys(b)[0])
                        return -1;
                    if (Object.keys(a)[0] > Object.keys(b)[0])
                        return 1;
                    return 0;
                });

                options.unshift({[dictionary['all']]: -1});
                ui.push({
                    'method': function(value) {
                        currentFilters[filter] = value;
                        viz.data(filteredData());
                        viz.draw();
                    },
                    'label': dictionary[filter],
                    'type': 'drop',
                    'value': options
                });
            } else {
                for (id in otherMetadata[filter]) {
                    if (filter == 'occupation_family' && !validOccupations.hasOwnProperty(id))
                        continue;
                    options.push({'id': otherMetadata[filter][id]['name_' + lang], 'label': otherMetadata[filter][id]['name_' + lang]})
                }

                options.sort(function(a, b) {
                    if (a['label'] < b['label'])
                        return -1;
                    if (a['label'] > b['label'])
                        return 1;
                    return 0;
                });

                options.unshift({'id': -1, 'label': dictionary['all']});
                d3plus.form()
                    .container(d3.select('#controls'))
                    .data(options)
                    .id('id')
                    .text('label')
                    .title(dictionary[filter])
                    .type('drop')
                    .font({'size': 11})
                    .focus(-1, function(value) {
                        currentFilters[filter] = value;
                        viz.data(filteredData());
                        viz.draw();
                    })
                    .draw();
            }
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
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .id('id')
        .time('year')
        .color({'heatmap': ["#282F6B", "#B22200"],
                'value': value})
        .draw();

    var addForms = function() {
        if ($('#d3plus_drawer').length == 0){
            setTimeout(addForms, 1000);
            return;
        }

        $('#d3plus_drawer').append($('#controls').children());
        $('#controls').remove();
    };

    addForms();

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

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
         ajaxQueue(
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
