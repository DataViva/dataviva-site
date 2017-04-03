var stacked = document.getElementById('stacked'),
    dataset = stacked.getAttribute('dataset'),
    filters = stacked.getAttribute('filters'),
    area = stacked.getAttribute('area'),
    args = getUrlArgs(),
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][area] || [area],
    group = depths[0],
    values = stacked.getAttribute('values').split(' '),
    type = stacked.getAttribute('type').split(' '),
    lang = document.documentElement.lang;
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset],
    yearRange = args.hasOwnProperty('year') ? [0, +args['year']] : [0, 0],
    metadata = {},
    currentFilters = {},
    currentTitleAttrs = {'area': area, 'value': values[0]},
    baseTitle = '',
    baseSubtitle = '',
    stackedFilters = args['filters'] ? args['filters'].split('+') : [];

var buildData = function(apiData) {
    
    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = apiData.headers;

    apiData.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
                if (['wage', 'average_wage'].indexOf(header) >= 0)
                    dataItem[header] = +dataItem[header]
            });

            dataItem[DICT[dataset]['item_id'][area]] = dataItem[area];

            for (key in calcBasicValues) {
                dataItem[key] = calcBasicValues[key](dataItem);   
            }
            
            if (HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';

            depths.forEach(function(depth) {
                dataItem[depth] = metadata[depth][dataItem[depth]]['name_' + lang];
            });
            
            if(depths.indexOf(area) == -1) {
                dataItem[area] = metadata[area][dataItem[area]]['name_' + lang];
            }
            
            if (dataItem.microregion){
                dataItem.microregion = dataItem.microregion + ' ';
            } else if (dataItem.state){
                dataItem.state = ' ' + dataItem.state;
            }
            if (dataItem.month){
                dataItem.month = dataItem.year + "/" + dataItem.month + "/01";
            }

            data.push(dataItem);
        } catch(e) {
        };
    });

    return data;
}

var loadViz = function (data){
    var hasIdLabel = function() {
        return DICT.hasOwnProperty(dataset) && DICT[dataset].hasOwnProperty('item_id') && DICT[dataset]['item_id'].hasOwnProperty(area);
    };

    var tooltipBuilder = function() {
        return {
            'short': {
                '': hasIdLabel() ? DICT[dataset]['item_id'][area] : 'id',
                [dictionary['basic_values']]: [values[0]]
            },
            'long': {
                '': hasIdLabel() ? DICT[dataset]['item_id'][area] : 'id',
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var uiBuilder = function() {
        ui = [];
        var config = {
            'id': 'id',
            'text': 'label',
            'font': {'size': 11},
            'container': d3.select('#controls'),
            'search': false
        };

        ui.push( {
            "label": "Layout",
            "type" : "drop",
            "value" : [
                {
                    [dictionary['year']]: "linear"
                }, 
                {
                    [dictionary['market-share']]: "share"
                }
            ],
            "method" : function(value, viz){
                viz.y({
                    "scale": value
                })
                .draw();
            }
        });

        ui.push({
            "label": dictionary['sort'],
            "type": "drop",
            "value": [
                {
                    [dictionary['desc']] : "desc"
                },
                {
                    [dictionary['asc']] : "asc"
                }
            ],
            "method": function(value, viz){
                viz.order({
                    "sort": value
                }).draw();
            }
        });

        ui.push({
            "label": dictionary['Order'],
            "type": "drop",
            "value": [
                {
                    [dictionary['value']] : "value"
                },
                {
                    [dictionary['name']] : "name"
                }
            ],
            "method": function(value, viz){

                if (value == "value"){
                    value = viz.y();
                }
                else {
                    value = viz.id();
                }

                viz.order({
                    "value": value
                }).draw();
            }
        });

        if (dataset == 'secex'){
            ui.push({
                "label": dictionary['time-resolution'],
                "value": [
                    {
                        [dictionary['year']]: "year"
                    },
                    {
                        [dictionary['month']]: "month"
                    }
                ],
                "method": function(value, viz){
                    viz.x({
                            "value": value,
                            "label": value
                    });
                    viz.time({
                        "value": value
                    }).draw();
                }
            });
        }

        if (dataset == 'rais'){
            var axis_values = [];

            for (var i = 0, len = values.length; i < len; i++) {
              axis_values.push({[dictionary[values[i]]] : values[i]})
            }

            ui.push({
                "label": dictionary['y-axis'],
                "type": "drop",
                "value": axis_values,
                "method": function(value, viz){

                    viz.y({
                        "value": value,
                        "label": yAxisLabelBuilder(value)
                    });

                    viz.order({
                        "value": value
                    }).draw();
                }
            });
        }

        if (values.length > 1) {
            d3plus.form()
                .config(config)
                .container(d3.select('#controls'))
                .data(values.map(function(value){
                    return {
                        id: value,
                        label: dictionary[value]
                    };
                }))
                .title(dictionary['value'])
                .type('drop')
                .font({'size': 11})
                .focus(-1, function(value) {
                    currentTitleAttrs['value'] = value;
                    viz.y(value)
                        .title({'total': {'prefix': dictionary[value] + ': '}})
                        .title(titleHelper())
                        .draw();
                })
                .draw();
        }

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

        stackedFilters.forEach(function(filter, j) {
            currentFilters[filter] = -1;
            var options = [];
            for (id in metadata[filter]) {
                options.push({'id': metadata[filter][id]['name_' + lang], 'label': metadata[filter][id]['name_' + lang]})
            }
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
        });

        return ui;
    }

    var titleHelper = function() {
        if (!baseTitle) {
            baseTitle = '<value> ' + dictionary['per'] + ' <area>';
        }

        var title = titleBuilder(baseTitle, baseSubtitle, currentTitleAttrs, dataset, getUrlArgs(), yearRange);

        return {
            'value': title['title'],
            'font': {'size': 22, 'align': 'left'},
            'sub': {'font': {'align': 'left'}, 'value': title['subtitle']},
        }
    };


    var yAxisLabelBuilder = function (type) {
        if (type == 'export')
        {
            (value = 'value_per_kg') ? dictionary['exports_weight'] : dictionary['exports'];  
        }   
        if (type == 'import') 
        {
            (value = 'value_per_kg') ? dictionary['imports_weight'] : dictionary['imports']; 
        } 
        if (type == 'balance') 
        {
            return dictionary['trade_value']
        } 
        if (type == 'jobs')
        { 
            return dictionary['total_jobs']
        } 
        if (type == 'wage')
        {
            return dictionary['wage']
        }
        if (type == 'establishment_count')
        {
            return dictionary['establishment_count']
        }

    }
    
    data_type = { "value": values[0], "label": (type == "" ? yAxisLabelBuilder(values[0]) : yAxisLabelBuilder(type))}

    var viz = d3plus.viz()
        .title({"value": "Inserir título", "font": {"family": "Times", "size": "24","align": "left"}})
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .y(data_type)  
        .x({"value": "year", "label": ""})
        .time({'value': 'year'})
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .title(titleHelper())
        .title({'total': {'font': {'align': 'left'}}})
        .title({'total': {'prefix': dictionary[values[0]] + ': '}})
        .tooltip(tooltipBuilder())
        .messages({'branding': true, 'style': 'large'})
        .ui(uiBuilder())
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .format(formatHelper())
        .depth(0, function(d) {
            currentTitleAttrs['area'] = depths[d];
            viz.title(titleHelper());
        })

        if (group) {
            viz.color(group);
        }

        if (depths[0] == '') {
            viz.id({'value': area})
        } else {
            viz.id(depths);
        }

        $('#stacked').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');

        viz.draw()

        toolsBuilder(stacked.id, viz, data, titleHelper().value);
}

var getUrls = function() {
    var dimensions = [dataset, (dataset == 'secex' ? 'month/year' : 'year'), area];

    depths.forEach(function(depth) {
        if (depth != area)
            dimensions.push(depth);
    });

    var urls = [
        'http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + area
    ];

    depths.forEach(function(depth) {
        urls.push('http://api.staging.dataviva.info/metadata/' + depth);
    });

    stackedFilters.forEach(function(filter){
        urls.push('http://api.staging.dataviva.info/metadata/' + filter);
    });
    
    return urls;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization'] + '...');

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            metadata[area] = responses[1];

            depths.concat(stackedFilters).forEach(function(attr, i) {
                metadata[attr] = responses[i + 2];
            });

            data = buildData(data);

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});
