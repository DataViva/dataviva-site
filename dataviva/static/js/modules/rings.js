var rings = document.getElementById('rings'),
    dataset = rings.getAttribute('dataset'),
    circles = rings.getAttribute('circles'),
    focus = rings.getAttribute('focus'),
    filters = rings.getAttribute('filters'),
    controls = true,
    currentYear = +getUrlArgs()['year'] || 0,
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset];

var buildData = function(apiResponse, circlesMetadata, connections) {

    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    };

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
                if (['wage', 'average_wage'].indexOf(header) >= 0)
                    dataItem[header] = +dataItem[header]
            });

            dataItem[DICT[dataset]['item_id'][circles]] = dataItem[circles];

            for (key in calcBasicValues) {
                dataItem[key] = calcBasicValues[key](dataItem);
            }

            dataItem[circles] = circlesMetadata[dataItem[circles]]['name_' + lang];

            var group = DEPTHS[dataset][circles][0]
            var groupId = circlesMetadata[dataItem[DICT[dataset]['item_id'][circles]]][group][DICT[dataset]['item_id'][group]]

            if (HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + groupId + '.png';

            connections.nodes.forEach(function(node){
                //slice -4 for secex
                if(node[DICT[dataset]['item_id'][circles]].slice(-4) == dataItem[DICT[dataset]['item_id'][circles]])
                    node[circles] = dataItem[circles]
            });

            if(dataItem[DICT[dataset]['item_id'][circles]] == focus)
                focus = dataItem[circles]

            data.push(dataItem);
        } catch(e) {

        };
    });

    connections.edges.forEach(function(edge){
        edge.source = connections.nodes[edge.source][circles];
        edge.target = connections.nodes[edge.target][circles];
    });

    return [data, connections.edges];
}

var loadViz = function(data, connections) {
    var uiBuilder = function() {
        ui = [];

        var args = getUrlArgs();
        if (args['year']) {
            ui.push({
                'method': function(value) {
                    if (value == args['year']) {
                        loadViz(data);
                    } else {
                        var loadingData = dataviva.ui.loading('#rings').text(dictionary['Downloading Additional Years'] + '...'),
                            copy = filters;

                        filters = filters.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}/, '?');

                        d3.json(getUrls()[0], function(allYearsData) {
                            allYearsData = buildData(allYearsData, circlesMetadata, connections);
                            viz.data(allYearsData);
                            viz.draw();

                            filters = copy;
                            currentYear = 0;
                            loadingData.hide();
                        });
                    }
                },
                'value': [args['year'], dictionary['all']],
                'label': dictionary['year']
            })
        }

        return ui;
    }

    var titleBuilder = function() {
        return {
            'value': 'Title',
            'font': {'size': 22, 'align': 'left'},
            'sub': {'font': {'align': 'left'}, 'value': 'Subtitle'},
            'total': {'font': {'align': 'left'}, 'value': true}
        }
    };

    var tooltipBuilder = function() {
        return {
            'short': {
                '': DICT[dataset]['item_id'][circles],
                [dictionary['basic_values']]: [focus] //export_val, import_val, export_kg, import_kg
            },
            'long': {
                '': DICT[dataset]['item_id'][circles],
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var timelineCallback = function(years) {
        currentYear = years.length == 1 ? years[0].getFullYear() : 0;
        toolsBuilder(viz, data, titleBuilder().value, uiBuilder());
    };

    var viz = d3plus.viz()
        .container('#rings')
        .type('rings')
        .data(data)
        .edges(connections)
        .focus(focus)
        .background('transparent')
        .time({'value': 'year', 'solo': {'callback': timelineCallback}})
        .icon({'value': 'icon', 'style': 'knockout'})
        //.legend({'filters': true, 'order': {'sort': 'asc', 'value': 'id'}})
        .color({'scale':'category20', 'value': circles})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large' })
        .title(titleBuilder())
        .id(circles)
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

    viz.draw();

    //refresh button not working
    toolsBuilder(viz, data, titleBuilder().value, uiBuilder());
};

var getUrls = function() {
    var dimensions = [dataset, 'year', circles];

    //http://api.staging.dataviva.info/secex/year/product/type/?year=2015
    // if (dataset == 'secex')
    //     dimensions.push('type') // exports and imports separately

    //http://api.staging.dataviva.info/rais/year/occupation_family/?year=2014&count=establishment

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + circles
    ];

    if (dataset == 'secex')
        urls.push('/' + lang + '/rings/networks/hs/');
        //cbo, cnae, hs, isic

    return urls;
};

var circlesMetadata = [];

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(),
        function(responses) {
            var data = responses[0];
            circlesMetadata = responses[1];
            connections = responses[2];

            data = buildData(data, circlesMetadata, connections);

            loadViz(data[0], data[1]);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});
