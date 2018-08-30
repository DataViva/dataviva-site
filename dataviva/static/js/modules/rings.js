var rings = document.getElementById('rings'),
    dataset = rings.getAttribute('dataset'),
    circles = rings.getAttribute('circles'),
    focus = rings.getAttribute('focus'),
    filters = rings.getAttribute('filters'),
    baseTitle = rings.getAttribute('graph-title'),
    baseSubtitle = rings.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    selectedYears = [0, args['year']] || [0, 2014],
    yearsRange = [],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][circles] || [circles],
    group = depths[0],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
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
            dataItem['edge_label'] = dataItem[circles];
            dataItem[circles] = circlesMetadata[dataItem[circles]]['name_' + lang];
            dataItem[group] = circlesMetadata[dataItem[ID_LABELS[group]]][group]['id'];

            if (COLORS.hasOwnProperty(group))
                dataItem['color'] = COLORS[group][dataItem[group]];

            if (HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            
            for (key in calcBasicValues) {
                dataItem[key] = calcBasicValues[key](dataItem);
            }

            data.push(dataItem);

        } catch(e) {};

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

var formatEdgesLabels = function() {
    return {
        'text': function(text, params) {
            if(params.key == 'edge_label' && text in circlesMetadata )
                return circlesMetadata[text]['name_' + lang];
            return dictionary[text] || text;
        }
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
            var options = [];
            yearsRange.forEach(function(item) {
                options.push({'id': item, 'label': item.toString()});
            });

            d3plus.form()
                .config(config)
                .data(options)
                .title(dictionary['year'])
                .type(options.length > 3 ? 'drop' : 'toggle')
                .focus(Number(args['year']), function(year) {
                        var loadingData = dataviva.ui.loading('#rings').text(dictionary['Downloading Additional Year'] + '...');
                        d3.select('.loading').style('background-color', '#fff');
                        window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '/&year=' + year).replace(/\?year=[0-9]{4}/, '?year=' + year);
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
        toolsBuilder('rings', viz, data, titleHelper(selectedYears).value);
        viz.title(titleHelper(selectedYears));
    };

    var viz = d3plus.viz()
        .container('#rings')
        .type('rings')
        .data(data)
        .edges(connections.edges)
        .focus(focus)
        .id('edge_label')
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
        .format(formatEdgesLabels())

    if (COLORS.hasOwnProperty(group)) {
        viz.attrs(COLORS[group]);
        viz.color('color');
    } else
        viz.color({'scale':'category20', 'value': args['color'] || depths[0]});

    uiBuilder();
    $('#rings').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');
    viz.draw();

    if ($('#controls').css('display') == 'none')
        $('#controls').fadeToggle();

    toolsBuilder('rings', viz, data, titleHelper(selectedYears).value);
};

var getUrls = function() {
    var dimensions = [dataset, 'year', circles];

    if (dataset == 'secex')
        dimensions.push('type')

    var urls = [api_url + dimensions.join('/') + '/?' + filters,
        api_url + 'metadata/' + circles,
        api_url + 'years/' + dataset
    ];

    var connectionsHelper = {
        'product': 'api_hs',
        'occupation_family': 'api_cbo',
        'industry_class': 'api_cnae'
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
            range = responses[2];
            connections = responses[3];

            yearsRange = range.years;
            data = buildData(data, circlesMetadata);

            if(dataset == 'secex')
                data = expandedData(data);

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
      requested by '/rings/networks/<id>' (id = hs,cnae or cbo) in 'rings/views.py'
    - Funcion 'expandedData' unifies data in a single set after performing
      the calculation of export and import values separately for SECEX 

{
    "nodes":[
        {
            "y":753.5362439817109, //node position in space, unused in rings
            "x":1553.2536950412032,
            "<id>":"<id_value>" //hs: "hs_id":"6208", cnae: "cnae_id":"31021", cbo: "cbo_id": "7661"
        },
        ...
    ],
    "edges":[
        {
            "source":"<id_value>",
            "proximity":"<value>",
            "target":"<id_value>"
        },
        ...
    ]
}

*/
