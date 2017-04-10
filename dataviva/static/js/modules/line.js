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
    yValues = args.hasOwnProperty('values') ? args['values'].split('+') : SIZES[dataset][yValue] || [yValue],
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
    currentFilters = {},
    currentTitleAttrs = {'yValue': yValue, 'Line': line}
    metadata = {},
    balance = line == 'type' ? true : false;

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

            if (balance)
                dataItem['icon'] = '/static/img/icons/balance/' + dataItem['type'] + '_val.png';
            else {
                depths.forEach(function(depth) {
                    if (depth != line)
                        dataItem[depth] = metadata[line][dataItem[line]][depth]['name_' + lang];
                    else 
                        dataItem[line] = metadata[line][dataItem[line]]['name_' + lang];
                });
            }

            if (dataItem['month'])
                dataItem['date'] = string2date(dataItem['year'] + '-' + dataItem['month'])
            data.push(dataItem);

        } catch(e) {};
    });

    return data;
}

var firstYear = function(data){
    var minYear = 9999;

    data.forEach(function(item){
        if(item.year < minYear)
            minYear = item.year;
    });

    return minYear;
};

var lastYear = function(data){
    var maxYear = 0;

    data.forEach(function(item){
        if(item.year > maxYear)
            maxYear = item.year;
    });

    return maxYear;
};

var allDates = function(minYear, maxYear, hasMonth){

        var dates = [];
        
        if (hasMonth){
            var months = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
                for(var year = minYear; year <= maxYear; year++){
                    months.forEach(function(month){
                        dates.push(new Date(year, month));
                    })
                }
        }
        else {
            for(var year = minYear; year <= maxYear; year++){
                dates.push(year);
            }
        }

    return dates;
};

/* The values are set as 1 because the logarithmic scale on the d3plus line chart 
does not work when the data has more than one value equal to 0.*/

FAKE_VALUE = 0.0833;

var fillMissingDates = function(data){
    var lines = new Set();
    var check = {};
    var hasMonth = data[0]["month"] == undefined ? false : true;

    data.forEach(function(item){
        lines.add(item[line]);

        if(check[item[line]] == undefined)
            check[item[line]] = {};

        check[item[line]][item.date] = true;
    });

    var dates = allDates(firstYear(data), lastYear(data), hasMonth);
    lines = Array.from(lines);

    dates.forEach(function(date){
        lines.forEach(function(lineValue){
            if(check[lineValue][date] == undefined){
                var dataItem = {};

                if(hasMonth){
                    dataItem['date'] = date;
                    dataItem['year'] = date.getFullYear();
                    dataItem['month'] = date.getMonth() + 1;
                    dataItem[line] = lineValue;

                } else {
                    dataItem['year'] = date;
                    dataItem[line] = lineValue;
                }

                yValues.forEach(function(value){
                    dataItem[value] = FAKE_VALUE;
                });

                data.push(dataItem);
            }
        });
    });

    return data;
};

var buildTradeBalanceData = function(data){
    //return data;
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

        // Adds values selector
        if (yValues.length > 1) {
            var options = [];
            yValues.forEach(function(item) {
                options.push({'id': item, 'label': dictionary[item]});
            });

            d3plus.form()
                .config(config)
                .data(options)
                .title(dictionary['values'])
                .type(options.length > 3 ? 'drop' : 'toggle')
                .focus(yValue, function(value) {
                    currentTitleAttrs['size'] = value;
                    viz.y({
                        'value': value
                    })
                    .draw();
                })
                .draw();
        }

        // Adds trade balance selector
        if (balance) {
            d3plus.form()
                .config(config)
                .data([{'id': 'value', 'label': dictionary['value']}, {'id': 'balance', 'label': dictionary['trade_balance']}])
                .title(dictionary['depth'])
                .type('toggle')
                .focus(dictionary['value'] ? 'value' : 'balance', function(value) {
                    //Adicionar campo 'balance' ao data ou criar outro conjunto de dados balanceData?
                    viz.y({
                        'value': value
                    });
                    viz.data(balanceData)
                    viz.draw();
                })
                .draw();
        }

        // Adds time resolution selector
        if (dataset == 'secex') {
            d3plus.form()
                .config(config)
                .data([{'id': 'year', 'label': dictionary['year']}, {'id': 'date', 'label': dictionary['month']}])
                .title(dictionary['time_resolution'])
                .type('toggle')
                .focus(dictionary['year'] ? 'year' : 'date', function(value) {
                    viz.x({
                        'value': value
                    });
                    viz.time({
                        'value': value
                    })
                    viz.draw();
                })
                .draw();

            d3plus.form()
                .config(config)
                .data([{'id': 'linear', 'label': dictionary['linear']}, {'id': 'log', 'label': dictionary['log']}])
                .title(dictionary['scale'])
                .type('toggle')
                .focus(dictionary['linear'] ? 'linear' : 'log', function(value) {
                    viz.y({
                        'scale': value
                    });
                    viz.draw();
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
        .ui(uiBuilder())
        .axes({'background': {'color': '#FFFFFF'}});

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

    if (!balance) urls.push(API_DOMAIN + '/metadata/' + line);

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
            data = fillMissingDates(data);

            // if (balance)
            //     data.sort(function(a,b) {return (a['date'] > b['date']) ? 1 : ((b['date'] > a['date']) ? -1 : 0);})
            //     data = buildTradeBalanceData(data);
            //     loadViz(balanceData);


            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});

// Tasks to do:

// Geral:
// 1. Testar todas as bases de dados
// 2. Valores Anuais (Padrão) e Mensais para SECEX (Seletores UI) >> DONE
// 3. Verificar tooltips:
//      - Valores;
//      - Ícones para países;
// 4. Rótulos dos eixos.

// Modelo: http://localhost:5000/en/product/021201/trade-partner?menu=exports-destination-line&url=line%2Fsecex%2Fall%2F021201%2Fall%2Fwld%2F%3Fy%3Dexport_val%26color%3Dcolor
// URL: http://localhost:5000/en/line/secex/country/value?values=value+kg&product=021201&type=export

// Gráfico de Balança Comercial:
// 1. Interpolar dados faltantes >> DONE !FAKE_VALUE = 1 para mensal, quando agrega por anual dado é sumarizado para 12.
// 2. Calcular Balança Comercial (line-bk.js).

// Modelo: http://localhost:5000/en/product/021201/trade-partner?menu=trade-balance-product-line&url=line%2Fsecex%2Fall%2F021201%2Fall%2Fbalance%2F%3Ftime%3Dyear
// URL: http://localhost:5000/en/line/secex/type/value?values=value+kg&product=021201

//Testar Interpolação:
// Modelo: http://localhost:5000/en/product/021201/trade-partner?bra_id=4mg030000
// URL: http://localhost:5000/en/line/secex/type/value?values=value+kg&product=021201&id_ibge=3106200
