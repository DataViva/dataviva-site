var tree_map = document.getElementById('tree_map'),
    dataset = tree_map.getAttribute('dataset'),
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    baseTitle = tree_map.getAttribute('graph-title'),
    baseSubtitle = tree_map.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    yearRange = [Number.POSITIVE_INFINITY, 0],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][squares] || [squares],
    hierarchy = args.hasOwnProperty('hierarchy') && args['hierarchy'] == 'false' ? false : true;
    zoom = args.hasOwnProperty('zoom') && args['zoom'] == 'true' ? true : false;
    group = depths[0],
    sizes = args.hasOwnProperty('sizes') ? args['sizes'].split('+') : SIZES[dataset][squares] || [size],
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
    currentFilters = {},
    currentTitleAttrs = {'size': size, 'shapes': squares}
    metadata = {};

if (depths.length > 1)
    currentTitleAttrs['depth'] = depths[0];

var buildData = function(apiResponse) {

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

            if (COLORS.hasOwnProperty(group))
                dataItem['color'] = COLORS[group][dataItem[group]];

            if (HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            
            if (ID_LABELS.hasOwnProperty(squares))
                dataItem[dictionary[ID_LABELS[squares]]] = dataItem[squares];
            else
                dataItem['id'] = dataItem[squares];

            for (key in calcBasicValues)
                dataItem[key] = calcBasicValues[key](dataItem);

            depths.forEach(function(depth) {
                if (depth != squares)
                    dataItem[depth] = metadata[squares][dataItem[squares]][depth]['name_' + lang];
                    //dataItem[depth] = metadata[depth][dataItem[depth]]['name_' + lang];
            });
           
            dataItem[squares] = metadata[squares][dataItem[squares]]['name_' + lang];

            if (dataItem.hasOwnProperty('year') && dataItem['year'] > yearRange[1])
                yearRange[1] = dataItem['year'];
            else if (dataItem.hasOwnProperty('year') && dataItem['year'] < yearRange[0])
                yearRange[0] = dataItem['year'];
            
            data.push(dataItem);

        } catch(e) {
        };
    });

    // Removes depths that all data items are part of
    // For example, if data is filtered by state, there is no reason to have region or state as depths, since all data is from the same state and region
    if (hierarchy && depths.length > 1) {
        var invalidDepths = [];
        depths.forEach(function(depth) {
            if (depth != squares) {
                var valid = false;
                for (var i = 1; i < data.length; i++) {
                    if (data[i][depth] != data[i-1][depth]) {
                        valid = true;
                        break;
                    }
                }
                if (!valid)
                    invalidDepths.push(depth);
            }
        });
        invalidDepths.forEach(function(depth) {
            depths.splice(depths.indexOf(depth), 1);
        });
    }

    if (yearRange[0] == yearRange[1])
        yearRange[0] = 0;
    
    return data;
}

var loadViz = function(data) {
    var uiBuilder = function() {
        var config = {
                'id': 'id',
                'text': 'label',
                'font': {'size': 11},
                'container': d3.select('#controls'),
                'search': false,
            };

        // Adds depth selector
        if (depths.length > 1) {
            var options = [];
            if (hierarchy) {
                depths.forEach(function(item) {
                    options.push({'id': item, 'label': dictionary[item]});
                });

                d3plus.form()
                    .config(config)
                    .data(options)
                    .title(dictionary['depth'])
                    .type(options.length > 3 ? 'drop' : 'toggle')
                    .focus(squares, function(value) {
                        currentTitleAttrs['shapes'] = value;
                        viz.depth(depths.indexOf(value))
                            .title(titleHelper(yearRange))
                            .draw();
                    })
                    .draw();
            } else {
                depths.forEach(function(item) {
                    if (item != squares)
                        options.push({'id': item, 'label': dictionary[item]});
                });

                d3plus.form()
                    .config(config)
                    .data(options)
                    .title(dictionary['drawer_color_by'])
                    .type(depths.length > 3 ? 'drop' : 'toggle')
                    .focus(options[0]['id'], function(value) {
                        currentTitleAttrs['shapes'] = value;
                        viz.data(data)
                            .id([value, squares])
                            .color(value)
                            .title(titleHelper(yearRange))
                            .draw();
                    })
                    .draw();

                d3plus.form()
                    .config(config)
                    .data([{'id': 0, 'label': dictionary['yes']}, {'id': 1, 'label': dictionary['no']}])
                    .title(dictionary['drawer_group'])
                    .type('toggle')
                    .focus(1, function(value) {
                        viz.depth(value)
                        viz.draw();
                    })
                    .draw();
            }
        }

        // Adds size selector
        if (sizes.length > 1) {
            var options = [];
            sizes.forEach(function(item) {
                options.push({'id': item, 'label': dictionary[item]});
            });

            d3plus.form()
                .config(config)
                .data(options)
                .title(dictionary['sizing'])
                .type(options.length > 3 ? 'drop' : 'toggle')
                .focus(size, function(value) {
                    currentTitleAttrs['size'] = value;
                    viz.size(value)
                        .title(titleHelper(yearRange))
                        .title({'total': {'prefix': dictionary[value] + ': '}})
                        .draw();
                })
                .draw();
        }

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
                        var loadingData = dataviva.ui.loading('#tree_map').text(dictionary['Downloading Additional Years'] + '...');
                        d3.select('.loading').style('background-color', '#fff');
                        window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}/, '?');
                    }
                })
                .draw();
        }

        // Adds filters selector        
        var filteredData = function(filter, value) {
            currentFilters[filter] = value;
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


        filters.forEach(function(filter) {
            if (filter == 'attention_level') {
                currentFilters['ambulatory_attention'] = -1;
                currentFilters['hospital_attention'] = -1;

                var filterValues = [
                    [-1, -1], // Todos 
                    [0, 0],   // Nenhum
                    [0, 1],   // Hospitalar
                    [1, 0],   // Ambulatorial
                    [1, 1]    // Ambulatorial/Hospitalar
                ];

                var options = [
                    {'id': 0, 'label': dictionary['all']},
                    {'id': 1, 'label': dictionary['none']},
                    {'id': 2, 'label': dictionary['hospital']},
                    {'id': 3, 'label': dictionary['ambulatory']},
                    {'id': 4, 'label': dictionary['ambulatory/hospital']},
                ];

                d3plus.form()
                    .config(config)
                    .container(d3.select('#controls'))
                    .data(options)
                    .title(dictionary['attention_level'])
                    .type('drop')
                    .focus(0, function(value) {
                        viz.data(filteredData('ambulatory_attention', filterValues[value][0]))
                        viz.data(filteredData('hospital_attention', filterValues[value][1]))
                        viz.draw();
                    })
                    .draw();
            } else {
                currentFilters[filter] = -1;
                var options = [];
                for (id in metadata[filter]) {
                    options.push({'id': id, 'label': metadata[filter][id]['name_' + lang]})
                }

                options = options.sort(function(a, b) {
                    return (a.label.toLowerCase() < b.label.toLowerCase()) ? -1 : 1;
                });

                options.unshift({'id': -1, 'label': dictionary['all']});

                d3plus.form()
                    .config(config)
                    .container(d3.select('#controls'))
                    .data(options)
                    .title(dictionary[filter])
                    .type('drop')
                    .font({'size': 11})
                    .focus(-1, function(value) {
                        viz.data(filteredData(filter, value));
                        viz.draw();
                    })
                    .draw();
            }
        });      
    };

    var titleHelper = function(years) {
        if (!baseTitle) {
            var genericTitle = hierarchy ? '<size> ' + dictionary['per'] + ' <shapes>' : '<size> ' + dictionary['per'] + ' <shapes>';
            if (depths.length > 1 && currentTitleAttrs['shapes'] != currentTitleAttrs['shapes'])
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
                '': ID_LABELS.hasOwnProperty(squares) ? dictionary[ID_LABELS[squares]] : 'id',
                [dictionary['basic_values']]: [size]
            },
            'long': {
                '': ID_LABELS.hasOwnProperty(squares) ? dictionary[ID_LABELS[squares]] : 'id',
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var timelineCallback = function(years) {
        var selectedYears = [];
        if (!years.length)
            selectedYears = yearRange;
        else if (years.length == 1)
            selectedYears = [0, years[0].getFullYear()];
        else
            selectedYears = [years[0].getFullYear(), years[years.length - 1].getFullYear()]
        toolsBuilder('tree_map', viz, data, titleHelper(selectedYears).value);
        viz.title(titleHelper(selectedYears));
    };

    var viz = d3plus.viz()
        .container('#tree_map')
        .data({'value': data, 'padding': 0})
        .type('tree_map')
        .size(size)
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time({'value': 'year', 'solo': {'value': yearRange[1], 'callback': timelineCallback}})
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .legend({'filters': true, 'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleHelper([0, yearRange[1]]))
        .title({'total': {'font': {'align': 'left'}}})
        .title({'total': {'prefix': dictionary[size] + ': '}})
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

    if (hierarchy) {
        viz.id(depths); 
        viz.depth(args['depth'] || depths.indexOf(squares));
        viz.zoom(zoom || false);
    } else {
        viz.id([args['depth'] || depths[0], squares]);
        viz.depth(1);
        viz.zoom(zoom || true);
    }

    if (COLORS.hasOwnProperty(group)) {
        viz.attrs(COLORS[group]);
        viz.color('color');
    } else {
        viz.color({'scale':'category20', 'value': args['color'] || depths[0]});
    }

    $('#tree_map').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');
    
    viz.draw();

    toolsBuilder('tree_map', viz, data, titleHelper(yearRange).value);
};


var getUrls = function() {
    var dimensions = [dataset, 'year', squares],
    metadataAttrs = [];
    
    depths.concat(filters).forEach(function(attr) {
        if (attr != squares && dimensions.indexOf(attr) == -1) {
            if (attr == 'attention_level') {
                dimensions.push('ambulatory_attention', 'hospital_attention');
            } else {
                metadataAttrs.push(attr);
                dimensions.push(attr);
            }
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + tree_map.getAttribute('filters'),
        API_DOMAIN + '/metadata/' + squares
    ];

    metadataAttrs.forEach(function(attr) {
        urls.push(API_DOMAIN + '/metadata/' + attr)
    });

    return urls;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            metadata[squares] = responses[1];

            var offset = 0;
            depths.concat(filters).forEach(function(attr, i) {
                if (attr != 'attention_level') {
                    if (!metadata.hasOwnProperty(attr)) {
                         metadata[attr] = responses[i-offset+2];
                    } else {
                        offset++;
                    }       
                }
            });

            data = buildData(data);
            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        },
        function(error) {
            loading.text(dictionary['Unable to load visualization']);
        }
    );
});
