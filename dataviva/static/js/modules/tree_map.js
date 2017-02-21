var tree_map = document.getElementById('tree_map'),
    dataset = tree_map.getAttribute('dataset'),
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    filters = tree_map.getAttribute('filters'),
    baseTitle = tree_map.getAttribute('graph-title'),
    baseSubtitle = tree_map.getAttribute('graph-subtitle'),
    yearRange = getUrlArgs()['year'] ? [0, +getUrlArgs()['year']] : [0, 0],
    depths = DEPTHS[dataset][squares],
    group = depths[0],
    sizes = SIZES[dataset][squares],
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset];

var buildData = function(apiResponse, squaresMetadata) {

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
                if (['wage', 'average_wage'].indexOf(header) >= 0)
                    dataItem[header] = +dataItem[header]
            });

            if (group && HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            
            if (squares in DICT[dataset]['item_id'])
                dataItem[DICT[dataset]['item_id'][squares]] = dataItem[squares];

            for (key in calcBasicValues)
                dataItem[key] = calcBasicValues[key](dataItem);

            depths.forEach(function(depth) {
                if (depth != squares)
                    dataItem[depth] = squaresMetadata[dataItem[squares]][depth]['name_' + lang];
            });
           
            dataItem[squares] = squaresMetadata[dataItem[squares]]['name_' + lang];
            

            data.push(dataItem);
        } catch(e) {

        };
    });

    return data;
}

var loadViz = function(data) {
    var uiBuilder = function() {
        var ui = [];

        if (depths.length > 1) {
            var options = depths.slice(0);
            options.splice(options.indexOf(squares), 1);
            options.splice(0, 0, squares);
            options.forEach(function(item, i){
                options[i] = {[dictionary[item]] : item};
            });

            ui.push({
                'method': function(value) {
                    viz.depth(depths.indexOf(value));
                    viz.title(titleHelper(value));
                    viz.draw();
                },
                'type': options.length > 3 ? 'drop' : '',
                'label': dictionary['depth'],
                'value': options
            });
        }

        if (sizes.length > 1) {
            var options = [];
            sizes.forEach(function(item) {
                options.push({[dictionary[item]]: item});
            });

            ui.push({
                'method' : 'size',
                'type': options.length > 3 ? 'drop' : '',
                'label': dictionary['sizing'],
                'value' : options
            });
        }

        var args = getUrlArgs();
        if (args['year']) {
            ui.push({
                'method': function(value) {
                    if (value == args['year']) {
                        loadViz(data);
                    } else {
                        var loadingData = dataviva.ui.loading('#tree_map').text(dictionary['Downloading Additional Years'] + '...');
                        window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}/, '?');
                    }
                },
                'value': [args['year'], dictionary['all']],
                'label': dictionary['year']
            })
        }

        return ui;
    }

    var titleHelper = function(depth) {
        var title = titleBuilder(depth, dataset, getUrlArgs(), yearRange);
        return {
            'value': title['title'],
            'font': {'size': 22, 'align': 'left'},
            'sub': {'font': {'align': 'left'}, 'value': title['subtitle']},
            'total': {'font': {'align': 'left'}, 'value': true}
        }
    };

    var tooltipBuilder = function() {
        return {
            'short': {
                '': DICT[dataset]['item_id'][squares],
                [dictionary['basic_values']]: [size]
            },
            'long': {
                '': DICT[dataset]['item_id'][squares],
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var timelineCallback = function(years) {
        yearRange = years.length == 1 ? [0, years[0].getFullYear()] : [years[0].getFullYear(), years[years.length - 1].getFullYear()];
        toolsBuilder(viz, data, titleHelper().value, uiBuilder());
        viz.title(titleHelper());
    };

    var viz = d3plus.viz()
        .container('#tree_map')
        .data({'value': data, 'padding': 0})
        .type('tree_map')
        .size(size)
        .zoom(false)
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time({'value': 'year', 'solo': {'callback': timelineCallback}})
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .legend({'filters': true, 'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleHelper(squares))
        .id(depths)
        .depth(depths.indexOf(squares))
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

    viz.color(depths.length > 1 ? {'scale':'category20', 'value': group} : {'scale':'category20'});

    viz.draw();

    toolsBuilder(viz, data, titleHelper().value, uiBuilder());
};


var getUrls = function() {
    var dimensions = [dataset, 'year', squares];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length)
        dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != squares)
            dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + squares
    ];

    return urls;
};

var squaresMetadata = [];

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            squaresMetadata = responses[1];

            data = buildData(data, squaresMetadata);

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});
