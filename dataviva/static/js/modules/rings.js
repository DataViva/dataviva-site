var rings = document.getElementById('rings'),
    dataset = rings.getAttribute('dataset'),
    circles = rings.getAttribute('circles'),
    focus = rings.getAttribute('focus'),
    filters = rings.getAttribute('filters'),
    controls = true,
    currentYear = +getUrlArgs()['year'] || 0,
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset];

var buildData = function(apiResponse, circlesMetadata) {

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

    return data;
};

var expandedData = function(data) {

    var expandedData = [];

    data.forEach(function(item){
        if(item['type'] == 'export'){
            data.forEach(function(item2){
                if(item['product'] == item2['product'] && item2['type'] == 'import'){
                    item['exports_value'] = item['value'];
                    item['exports_weight'] = item['kg'];
                    item['imports_value'] = item2['value'];
                    item['imports_weight'] = item2['kg'];
                    item['imports_per_weight'] = item2['imports_per_weight'];

                    delete item['type'];
                    delete item['value'];
                    delete item['kg'];

                    expandedData.push(item);
                }
            });
        }
    });

    return expandedData;
};

var loadViz = function(data) {
    var uiBuilder = function() {
        ui = [];

        var args = getUrlArgs();
        if (args['year']) {
            ui.push({
                'method': function(value) {
                    if (value == args['year']) {
                        loadViz(data);
                    } else {
                        var loadingData = dataviva.ui.loading('#rings').text(dictionary['Downloading Additional Years'] + '...');
                        window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '').replace(/\year=[0-9]{4}/, '');
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
                [dictionary['basic_values']]: [focus]
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
        .edges(connections.edges)
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

    toolsBuilder(viz, data, titleBuilder().value, uiBuilder());
};

var getUrls = function() {
    var dimensions = [dataset, 'year', circles];

    if (dataset == 'secex')
        dimensions.push('type')

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + circles
    ];

    //http://api.staging.dataviva.info/secex/year/product/type/?year=2015
    //http://api.staging.dataviva.info/rais/year/occupation_family/?year=2014&count=establishment

    var connectionsHelper = {
        'product': 'hs',
        'occupation_family': 'cbo',
        'industry_class': 'cnae'
        //'': 'isic'
    };

    urls.push('/' + lang + '/rings/networks/' + connectionsHelper[circles] + '/');

    return urls;
};

var connections = [];
var circlesMetadata = [];

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(),
        function(responses) {
            var data = responses[0];
            circlesMetadata = responses[1];
            connections = responses[2];

            data = buildData(data, circlesMetadata);

            if(dataset == 'secex')
                data = expandedData(data);

            connections.edges.forEach(function(edge){
                edge.source = connections.nodes[edge.source][circles];
                edge.target = connections.nodes[edge.target][circles];
            });

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});
