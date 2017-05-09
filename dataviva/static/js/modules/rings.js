var rings = document.getElementById('rings'),
    dataset = rings.getAttribute('dataset'),
    circles = rings.getAttribute('circles'),
    focus = rings.getAttribute('focus'),
    filters = rings.getAttribute('filters'),
    baseTitle = rings.getAttribute('graph-title'),
    baseSubtitle = rings.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    yearRange = [Number.POSITIVE_INFINITY, 0],
    selectedYears = [],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][circles] || [circles],
    group = depths[0],
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset],
    currentTitleAttrs = {'circles': circles, 'focus': focus};

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

            dataItem[ID_LABELS[group]] = dataItem[circles];
            dataItem[circles] = circlesMetadata[dataItem[circles]]['name_' + lang];
            dataItem[group] = circlesMetadata[dataItem[ID_LABELS[group]]][group]['id'];

            if (COLORS.hasOwnProperty(group))
                    dataItem['color'] = COLORS[group][dataItem[group]];

            if (HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            
            for (key in calcBasicValues) {
                dataItem[key] = calcBasicValues[key](dataItem);
            }

            //Adds names to nodes IDs according to the rings circles (e.g., '021202' > 'Soybeans')
            connections.nodes.forEach(function(node){
                var nodeKey;
                if(circles == 'product')
                    nodeKey = node[ID_LABELS[group]].slice(-4);

                if(circles == 'occupation_family')
                    nodeKey = node[ID_LABELS[group]];

                if(circles == 'industry_class')
                    nodeKey = node[ID_LABELS[group].slice(-2)].substr(1);

                if(nodeKey == dataItem[ID_LABELS[group]])
                    node[circles] = dataItem[circles]
            });

            if(dataItem[ID_LABELS[group]] == focus)
                focus = dataItem[circles];

            if (dataItem.hasOwnProperty('year') && dataItem['year'] > yearRange[1])
                yearRange[1] = dataItem['year'];
            else if (dataItem.hasOwnProperty('year') && dataItem['year'] < yearRange[0])
                yearRange[0] = dataItem['year'];

            data.push(dataItem);

        } catch(e) {};

        if (yearRange[0] == yearRange[1])
        yearRange[0] = 0;

        selectedYears = [0, yearRange[1]];
    });

    return data;
};

var expandedData = function(data) {

    var expandedData = [];

    data.forEach(function(item){
        if(item['type'] == 'export'){
            data.forEach(function(importItem){
                if(item['product'] == importItem['product'] && importItem['type'] == 'import' && item['year'] == importItem['year']){
                    item['exports_value'] = item['value'];
                    item['exports_weight'] = item['kg'];
                    item['imports_value'] = importItem['value'];
                    item['imports_weight'] = importItem['kg'];
                    item['imports_per_weight'] = importItem['imports_per_weight'];

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

var connectionsData = function() {

    if(dataset == 'secex'){
        connections.edges.forEach(function(edge){
            edge.source = connections.nodes[edge.source][circles];
            edge.target = connections.nodes[edge.target][circles];
        });
    }

    if(dataset == 'rais'){
        var id = circles == 'occupation_family' ? 'cbo_id' : 'id';

        for (var i = 0; i < connections.edges.length; i++) {
            for (var j = 0; j < connections.nodes.length; j++) {
                if (connections.edges[i]['source'] == connections.nodes[j][id])
                    connections.edges[i]['source'] = connections.nodes[j][circles];

                if (connections.edges[i]['target'] == connections.nodes[j][id])
                    connections.edges[i]['target'] = connections.nodes[j][circles];
            };
        };
    }
};

var loadViz = function(data) {
    var uiBuilder = function() {
        var config = {
                'id': 'id',
                'text': 'label',
                'font': {'size': 11},
                'container': d3.select('#controls'),
                'search': false
            };

        // Adds year selector
        if (args['year']) {
            d3plus.form()
                .config(config)
                .data([{'id': 1, 'label': args['year']}, {'id': 0, 'label': dictionary['all']}])
                .title(dictionary['year'])
                .type('toggle')
                .focus(args['year'] ? 1 : 0, function(value) {
                     if (value) {
                        loadViz(data);
                    } else {
                        var loadingData = dataviva.ui.loading('#rings').text(dictionary['Downloading Additional Years'] + '...');
                        d3.select('.loading').style('background-color', '#fff');
                        window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}/, '?');
                    }
                })
                .draw();
        }
    }

    var titleHelper = function(years) {
        if (!baseTitle) {
            var genericTitle = '<circles> ' + dictionary['per'] + ' <focus>';
            if (depths.length > 1 && currentTitleAttrs['focus'] != currentTitleAttrs['focus'])
                genericTitle += '/<depth>';
        }

        var header = titleBuilder(!baseTitle ? genericTitle : baseTitle, baseSubtitle, currentTitleAttrs, dataset, getUrlArgs(), years);

        return {
            'value': header['title'],
            'font': {'size': 22, 'align': 'left'},
            'padding': 5,
            'sub': {'font': {'align': 'left'}, 'value': header['subtitle']},
            'width': window.innerWidth - d3.select('#tools').node().offsetWidth - 20
        };
    };

    var tooltipBuilder = function() {
        return {
            'short': {
                '': ID_LABELS[group],
                [dictionary['basic_values']]: [focus]
            },
            'long': {
                '': ID_LABELS[group],
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var timelineCallback = function(years) {
        if (!years.length)
            selectedYears = yearRange;
        else if (years.length == 1)
            selectedYears = [0, years[0].getFullYear()];
        else
            selectedYears = [years[0].getFullYear(), years[years.length - 1].getFullYear()]
        toolsBuilder('rings', viz, data, titleHelper(selectedYears).value);
        viz.title(titleHelper(selectedYears));
    };

    var viz = d3plus.viz()
        .container('#rings')
        .type('rings')
        .data(data)
        .edges(connections.edges)
        .focus(focus)
        .id(circles)
        .axes({'background': {'color': '#FFFFFF'}})
        .background('transparent')
        .time({'value': 'year', 'solo': {'callback': timelineCallback}})
        .icon({'value': 'icon', 'style': 'knockout'})
        .color({'scale':'category20', 'value': circles})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large' })
        .title(titleHelper(selectedYears))
        .title({'total': {'font': {'align': 'left'}}})
        .tooltip(tooltipBuilder())
        .format(formatHelper())

    if (COLORS.hasOwnProperty(group)) {
        viz.attrs(COLORS[group]);
        viz.color('color');
    } else
        viz.color({'scale':'category20', 'value': args['color'] || depths[0]});

    uiBuilder();
    $('#rings').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');
    viz.draw();

    if (document.getElementById('controls').style.display = 'none')
        $('#controls').fadeToggle();

    toolsBuilder('rings', viz, data, titleHelper(yearRange).value);
};

var getUrls = function() {
    var dimensions = [dataset, 'year', circles];

    if (dataset == 'secex')
        dimensions.push('type')

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + circles
    ];

    var connectionsHelper = {
        'product': 'hs',
        'occupation_family': 'cbo',
        'industry_class': 'cnae'
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

            connectionsData(data);
            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        },
        function(error) {
            loading.text(dictionary['Unable to load visualization']);
        }
    );
});

/*

:: Rings Graph General Informations ::

Appears in the categories: Occupation, Industry e Product
Data Bases usage: RAIS, SECEX
Especific conditions or variables:
    - Connections are pre calculated and requested in additional request:
      File located in '/static/json/networks/'' and 
      requested by '/rings/networks/' in 'rings/views.py'
    - Funcion 'expandedData' unifies data in a single set after performing
      the calculation of export and import values separately for SECEX

*/
