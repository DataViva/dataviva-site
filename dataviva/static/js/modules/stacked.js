var stacked = document.getElementById('stacked'),
    dataset = stacked.getAttribute('dataset'),
    filters = stacked.getAttribute('filters'),
    area = stacked.getAttribute('area'),
    depths = DEPTHS[dataset][area],
    group = depths[0],
    values = stacked.getAttribute('values').split(' '),
    type = stacked.getAttribute('type').split(' '),
    lang = document.documentElement.lang;
    basicValues = BASIC_VALUES[dataset],
    calcBasicValues = CALC_BASIC_VALUES[dataset];

var buildData = function(apiData, areaMetadata, groupMetadata) {
    
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

            depths.forEach(function(depth) {
                if (depth != area && depth != group) {
                    dataItem[depth] = areaMetadata[dataItem[area]][depth]['name_' + lang];
                }
            });
            
            dataItem[area] = areaMetadata[dataItem[area]]['name_' + lang];
            
            if (group) {
                if (HAS_ICONS.indexOf(group) >= 0)
                    dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
                dataItem[group] = groupMetadata[dataItem[group]]['name_' + lang];
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
                '': DICT[dataset]['item_id'][area],
                [dictionary['basic_values']]: 'value'
            },
            'long': {
                '': DICT[dataset]['item_id'][area],
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var uiBuilder = function() {
        ui = [];

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

        return ui;
    }

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
        .time("year")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .title({
            "sub": {"value" : "Inserir sub-título", "font": {"align": "left"}}
        })
        .tooltip(tooltipBuilder())
        .ui(uiBuilder())
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .format(formatHelper())

        if (group) {
            viz.color(group);
        }

        if (depths[0] == '') {
            viz.id({'value': area})
        } else {
            viz.id(depths);
        }

        viz.draw()

        toolsBuilder(stacked.id, viz, data, titleBuilder().value, uiBuilder());
}

var getUrls = function() {
    var dimensions = [dataset, (dataset == 'secex' ? 'month/year' : 'year'), area];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length)
        dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != area)
            dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + area
    ];

    if (group)
        urls.push('http://api.staging.dataviva.info/metadata/' + group);
    return urls;
};

var areaMetadata = [],
    groupMetadata = [];

var loading = dataviva.ui.loading('.loading').text(dictionary['loading'] + '...');


$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            areaMetadata = responses[1];
            if (group)
                groupMetadata = responses[2];

            data = buildData(data, areaMetadata, groupMetadata);

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});