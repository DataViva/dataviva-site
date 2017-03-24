var tree_map = document.getElementById('tree_map'),
    dataset = tree_map.getAttribute('dataset'),
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    apiFilters = tree_map.getAttribute('filters'),
    baseTitle = tree_map.getAttribute('graph-title'),
    baseSubtitle = tree_map.getAttribute('graph-subtitle');

var args = getUrlArgs(),
    yearRange = args['year'] ? [0, +args['year']] : [0, 0],
    depths = args['depths'] || DEPTHS[dataset][squares] || [squares],
    group = depths[0],
    sizes = args['sizes'] || SIZES[dataset][squares] || [size],
    colors = args['colors'] || COLORS[dataset][squares] || [],
    filters = args['filter'] ? args['filter'].split('+') : FILTERS[dataset][squares] || [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {};

var buildData = function(apiResponse, squaresMetadata, otherMetadata) {

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
                
                if (DIMENSION_COLOR[header]) {
                    dataItem['color'] = DIMENSION_COLOR[header][dataItem[header]];
                }
            });

            if (group && HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            
            if (squares in DICT[dataset]['item_id'])
                dataItem[DICT[dataset]['item_id'][squares]] = dataItem[squares];
            else
                dataItem['id'] = dataItem[squares];

            for (key in calcBasicValues)
                dataItem[key] = calcBasicValues[key](dataItem);


            if (dataset == 'cnes_establishment') {
                for (d in otherMetadata) {
                    dataItem[d] = otherMetadata[d][dataItem[d]]['name_' + lang];
                }
            } else {
                depths.forEach(function(depth) {
                    if (depth != squares)
                        dataItem[depth] = squaresMetadata[dataItem[squares]][depth]['name_' + lang];
                });      
            }
           
            dataItem[squares] = squaresMetadata[dataItem[squares]]['name_' + lang];
            data.push(dataItem);
        } catch(e) {

        };
    });

    return data;
}

var loadViz = function(data) {
    var moveToPos = function(pos, elem, array) {
        var newArray = array.slice(0);
        newArray.splice(newArray.indexOf(elem), 1);
        newArray.splice(pos, 0, elem);
        return newArray;
    };

    var uiBuilder = function() {
        var ui = [];

        // Adds depth selector
        if (depths.length > 1) {
            var options = moveToPos(0, getUrlArgs()['depth'] || squares, depths);           
            options.forEach(function(item, i) {
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

        // Adds size selector
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

        // Adds color by selector
        if (colors.length) {
            ui.push({
                'method': function(value) {
                    viz.data(data);
                    viz.id([value, squares]);
                    viz.color(value);
                    viz.draw();
                },
                'type': colors.length > 3 ? 'drop' : '',
                'label': dictionary['drawer_color_by'],
                'value': moveToPos(0, getUrlArgs()['color'] || colors[0], colors)
            });

            // Adds depth level selector
            if (depths.length <= 1) {
                var value;
                if (tree_map.getAttribute('depth') == squares)
                    value = [{[dictionary['no']]: 1}, {[dictionary['yes']]: 0}];
                else
                    value = [{[dictionary['yes']]: 0}, {[dictionary['no']]: 1}];
                
                ui.push({
                    'type': 'button',
                    'method': function(value) {
                        viz.depth(value).draw();
                    },
                    'label': dictionary['drawer_group'] + ' ' + dictionary[squares],
                    'value': value
                });
            }
        }

        // Adds year selector
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

        // Adds filters selector
        filters.forEach(function(filter) {        
            var options = [];
            for (id in otherMetadata[filter]) {
                options.push(otherMetadata[filter][id]['name_' + lang])
            }
            options.sort(function(a, b) {return a ? a.toUpperCase() > b.toUpperCase() : a});
            options.unshift({[dictionary['all']]: 0});

            ui.push({
                'method': function(value) {
                    viz.data(value ? data.filter(function(item) {return item[filter] == value}) : data);
                    viz.draw();
                },
                'type': 'drop',
                'label': dictionary[filter],
                'value': options
            });
        });

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
                '': DICT[dataset]['item_id'][squares] || 'id',
                [dictionary['basic_values']]: [size]
            },
            'long': {
                '': DICT[dataset]['item_id'][squares] || 'id',
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var timelineCallback = function(years) {
        if (!years.length)
            yearRange = [0, 0];
        else if (years.length == 1)
            yearRange = [0, years[0].getFullYear()];
        else
            yearRange = [years[0].getFullYear(), years[years.length - 1].getFullYear()]
        toolsBuilder(viz, data, titleHelper().value, uiBuilder());
        viz.title(titleHelper());
    };

    var viz = d3plus.viz()
        .container('#tree_map')
        .data({'value': data, 'padding': 0})
        .type('tree_map')
        .size(size)
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time({'value': 'year', 'solo': {'callback': timelineCallback}})
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .legend({'filters': true, 'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleHelper(squares))
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

    if (colors.length) {
        viz.id([args['color'] || colors[0], squares]);
        viz.depth(depths.indexOf(tree_map.getAttribute('depth')) || 1);
        viz.zoom(true);
    } else {
        viz.id(depths); 
        viz.depth(args['depth'] || depths.indexOf(squares));
        viz.zoom(false);
    }

    if (getUrlArgs()['color']) {
        viz.color({'scale':'category20', 'value': args['color']});
    }
    else {
        if (colors.length && depths.length == 1) {
            viz.color({'scale':'category20', 'value': args['color'] || colors[0]});
        } else if (depths.length > 1) {
            viz.color({'scale':'category20', 'value': group});
        } else {
            viz.color({'scale':'category20'});
        }
    }
    viz.draw();

    toolsBuilder(viz, data, titleHelper().value, uiBuilder());
};


var getUrls = function() {
    var dimensions = [dataset, 'year', squares];
    var metadata = [];
    
    depths.concat(colors).concat(filters).forEach(function(attr) {
        if (attr != squares && dimensions.indexOf(attr) == -1) {
            dimensions.push(attr);
            metadata.push(attr);
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + apiFilters,
        API_DOMAIN + '/metadata/' + squares
    ];

    if (dataset == 'cnes_establishment') {
        metadata.forEach(function(attr) {
            urls.push(API_DOMAIN + '/metadata/' + attr)
        });
    }

    return urls;
};

var squaresMetadata = [];

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            squaresMetadata = responses[1],
            otherMetadata = {};

            if (dataset == 'cnes_establishment') {
                var offset = 0;
                depths.concat(colors).concat(filters).forEach(function(depth, i) {
                    if (depth != squares)
                        otherMetadata[depth] = responses[2+i-offset];
                    else
                        offset = 1;
                });
            }

            data = buildData(data, squaresMetadata, otherMetadata);

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});
