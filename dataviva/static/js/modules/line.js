var lineGraph = document.getElementById('lineGraph'),
    dataset = lineGraph.getAttribute('dataset'),
    line = lineGraph.getAttribute('line'),
    yValue = lineGraph.getAttribute('y_value'),
    baseTitle = lineGraph.getAttribute('graph-title'),
    baseSubtitle = lineGraph.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    yearRange = args.hasOwnProperty('year') ? [0, +args['year']] : [0, 0],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][line] || [line],
    group = depths[0],
    yValues = args.hasOwnProperty('yValues') ? args['yValues'].split('+') : SIZES[dataset][yValue] || [yValue],
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
    currentFilters = {},
    currentTitleAttrs = {'yValue': yValue, 'Line': line}
    metadata = {},
    lastYear = 0;

function string2date(dateString) {
    dateString = dateString.split('-');
    var month = (dateString.length == 2 && dateString[1] !== '0') ? dateString[1] : 1;
    var year = dateString[0];
    return new Date(month + '/01/' + year)
}

var buildData = function(apiResponse){

    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item){
        try{
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
            });

            if (DICT.hasOwnProperty(dataset) && DICT[dataset].hasOwnProperty('item_id') && DICT[dataset]['item_id'].hasOwnProperty(line))
                dataItem[DICT[dataset]['item_id'][line]] = dataItem[line];
            else
                dataItem['id'] = dataItem[line];

            if(group && HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';

            for (key in calcBasicValues)
                dataItem[key] = calcBasicValues[key](dataItem);

            depths.forEach(function(depth) {
                if (depth != 'type'){ //Refatorar
                    if (depth != line)
                        dataItem[depth] = metadata[line][dataItem[line]][depth]['name_' + lang];
                    else 
                        dataItem[line] = metadata[line][dataItem[line]]['name_' + lang];
                }
            });

            //if(type == 'balance') dataItem['icon'] = '/static/img/icons/' + type + '/' + dataItem['type'] + '_val.png';

            dataItem['date'] = string2date(dataItem['year'] + '-' + dataItem['month'])
            data.push(dataItem);

            //if (dataItem.hasOwnProperty('year') && dataItem['year'] > lastYear)
                //lastYear = dataItem['year'];
        } catch(e) {

        };
    });

    return data;
}

var loadViz = function(data) {
    var uiBuilder = function() {
        var config = {
                'id': 'id',
                'text': 'label',
                'font': {'size': 11},
                'container': d3.select('#controls'),
                'search': false
            };
    
        if (dataset == 'secex') {
            d3plus.form()
                .config(config)
                .data([{'id': 1, 'label': dictionary['year']}, {'id': 0, 'label': dictionary['month']}])
                .title(dictionary['time_resolution'])
                .type('toggle')
                .focus(dictionary['year'] ? 1 : 0, function(value) {
                    debugger;
                    viz.x({
                        'value': 'month'
                    });
                    viz.draw();
                //      if (value) {
                //         loadViz(data);
                //     } else {
                //         var loadingData = dataviva.ui.loading('#tree_map').text(dictionary['Downloading Additional Years'] + '...');
                //         window.location.href = window.location.href.replace(/&year=[0-9]{4}/, '').replace(/\?year=[0-9]{4}/, '?');
                //     }
                })
                .draw();
        }
    };

    var hasIdLabel = function() {
        return DICT.hasOwnProperty(dataset) && DICT[dataset].hasOwnProperty('item_id') && DICT[dataset]['item_id'].hasOwnProperty(line);
    }

    var tooltipBuilder = function() {
        return {
            'short': {
                '': hasIdLabel() ? DICT[dataset]['item_id'][line] : 'id',
                [dictionary['basic_values']]: [yValue]
            },
            'long': {
                '': hasIdLabel() ? DICT[dataset]['item_id'][line] : 'id',
                [dictionary['basic_values']]: basicValues.concat(Object.keys(calcBasicValues))
            }
        }
    };

    var viz = d3plus.viz()
        .container('#lineGraph')
        .data({'value': data, 'padding': 0})
        .type('line')
        .shape({'interpolate': 'monotone'})
        .x({
            'value': 'year',
            'label': {'font': {'size': 20}},
            'ticks': {'font': {'size': 17}
            }
        })
        .y({
            'value': 'value',
            //'label': {'value': yAxisLabelBuilder(type), 'font': {'size': 20}},
            'ticks': {'font': {'size': 17}}
        })

        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time({'value': 'year'})
        .icon({'value': 'icon', 'style': 'knockout'})
        .legend({'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

        if (group){
            viz.id([group, line]);
            viz.color(group);
        } else {
            viz.id(line).color(line);
        }

        if (COLORS.hasOwnProperty(group)) {
            viz.attrs(COLORS[group]);
            viz.color('color');
        } else {
            viz.color({'scale':'category20', 'value': args['color'] || depths[0]});
        }

        $('#lineGraph').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');
    
    viz.draw();

};

var getUrls = function() {
    var dimensions = [dataset, (dataset == 'secex' ? 'month/year' : 'year'), line],
    metadataAttrs = [];
    
    depths.concat(filters).forEach(function(attr) {
        if (attr != line && dimensions.indexOf(attr) == -1) {
            dimensions.push(attr);
            metadataAttrs.push(attr);
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + lineGraph.getAttribute('filters')]

    if (line != 'type') urls.push(API_DOMAIN + '/metadata/' + line);

    return urls;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            metadata[line] = responses[1];

            data = buildData(data);
            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});

// Montar o gráfico:
// http://localhost:5000/en/product/021201/trade-partner?menu=exports-destination-line&url=line%2Fsecex%2Fall%2F021201%2Fall%2Fwld%2F%3Fy%3Dexport_val%26color%3Dcolor

// Url:
// http://localhost:5000/en/line/secex/country/value?product=021201&type=export

//ToDo:
// 1. Montar gráfico Anual (Padrão) e Mensal (Seletores UI).
// 2. Interpolar dados faltantes.
// 3. Calcular Balança Comercial.
// 4. Verificar tooltips:
//      - Valores;
//      - Ícones para países;