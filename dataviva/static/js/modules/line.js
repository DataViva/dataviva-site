var lineGraph = document.getElementById('lineGraph'),
    dataset = lineGraph.getAttribute('dataset'),
    line = lineGraph.getAttribute('line'),
    yValue = lineGraph.getAttribute('y_value'),
    baseTitle = lineGraph.getAttribute('graph-title'),
    baseSubtitle = lineGraph.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    yearRange = [Number.POSITIVE_INFINITY, 0],
    selectedYears = [],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][line] || [line],
    group = depths[0],
    yValues = args.hasOwnProperty('values') ? args['values'].split('+') : SIZES[dataset][yValue] || [yValue],
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
    currentFilters = {},
    currentTitleAttrs = {'yValue': yValue, 'line': line}
    metadata = {},
    balance = line == 'type' ? true : false,
    port = line == 'port' ? true : false,
    students = yValue == 'students_number' ? true : false,
    MAX_LINE_LIMIT = 10;

function string2date(dateString) {
    dateString = dateString.split('-');
    var month = (dateString.length == 2 && dateString[1] !== '0') ? dateString[1] : 1;
    var year = dateString[0];
    return new Date(month + '/01/' + year)
}

function buildYearRange(dataItem) {
    if (dataItem.hasOwnProperty('year') && dataItem['year'] > yearRange[1])
        yearRange[1] = dataItem['year'];
    else if (dataItem.hasOwnProperty('year') && dataItem['year'] < yearRange[0])
        yearRange[0] = dataItem['year'];
}

function buildStudentsData(data, dataItem) {
    var students_situation = ['enrolled', 'entrants', 'graduates'],
        partialArrayData = [];

    students_situation.forEach(function(situation){
        partialDataItem = {};
        partialDataItem['year'] = dataItem['year'];
        partialDataItem['students'] = situation
        partialDataItem['students_number'] = Number(dataItem[situation]);

        buildYearRange(partialDataItem);

        data.push(partialDataItem);
    });
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

            if (students)
                buildStudentsData(data, dataItem)

            else {

                if (ID_LABELS.hasOwnProperty(line))
                    dataItem[dictionary[ID_LABELS[line]]] = dataItem[line];
                else
                    dataItem['id'] = dataItem[line];

                if (COLORS.hasOwnProperty(group))
                    dataItem['color'] = COLORS[group][dataItem[group]];

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

                buildYearRange(dataItem);

                data.push(dataItem);
            }

        } catch(e) {};
    });

    if (yearRange[0] == yearRange[1])
        yearRange[0] = 0;

    selectedYears = [yearRange[0], yearRange[1]];

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

/* The values are set as 1 because the logarithmic scale on the d3plus
line chart does not work when the data has more than one value equal to 0.

Issue: FAKE_VALUE = 1 for the monthly period, when aggregated by annual period
the value is summarized to 12. */

FAKE_VALUE = 1;

var fillMissingDates = function(data){
    var lines = new Set(),
        check = {},
        hasMonth = false;
    
    if (data[0] != null)
        hasMonth = data[0]["month"] == undefined ? false : true;

    data.forEach(function(item){
        lines.add(item[line]);

        if(check[item[line]] == undefined)
            check[item[line]] = {};

        if(group)
            check[item[line]][group] = item[group];

        check[item[line]][item.date] = true;
    });

    var dates = allDates(firstYear(data), lastYear(data), hasMonth);
    lines = Array.from(lines);

    dates.forEach(function(date){
        lines.forEach(function(lineValue){
            if(check[lineValue][date] == undefined){
                var dataItem = {};

                dataItem[group] = check[lineValue][group];

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
    data.forEach(function(item, index, allItems) {
        var tradeBalance = {},
            nextItem = allItems[index + 1];
        
        if (index % 2 !== 0 || nextItem === undefined)
            return;

        try{
            tradeBalance['date'] = string2date(item['year'] + '-' + item['month'])
            tradeBalance['year'] = item['year'];
            tradeBalance['month'] = item['month'];

            if(item['year'] == nextItem['year'] && item['month'] == nextItem['month'] &&
                item['type'] != nextItem['type']){

                if(item['type'] == 'export'){
                    tradeBalance['value'] = item['value'] - nextItem['value'];
                    tradeBalance['kg'] = item['kg'] - nextItem['kg']
                }
                else{
                    tradeBalance['value'] =  nextItem['value'] - item['value'];
                    tradeBalance['kg'] =  nextItem['kg'] - item['kg'];
                }

                tradeBalance['trade_balance'] = 'trade_balance'
            }

            data.push(tradeBalance);
            index = index + 1;
            return;
            
        } catch(e) {};
    });

    return data;
};

var groupDataByLine = function(data){
    var sumByItem = {};

    data.forEach(function(item){
        if(sumByItem[item[line]] == undefined)
            sumByItem[item[line]] = {
                "sum": 0,
                "name": item[line]
            };

        sumByItem[item[line]].sum += item[yValue];
    });

    var list = [];

    for(var item in sumByItem){
        list.push({
            name: sumByItem[item].name,
            sum: sumByItem[item].sum
        });
    }

    return list;
}

var getTopCurrentLines = function(groupedData){
    var compare = function(a, b){
        if(a.sum < b.sum)
            return 1;
        if(a.sum > b.sum)
            return -1;

        return 0;
    }

    var list = groupedData.sort(compare).slice(0, MAX_LINE_LIMIT);

    var selected = list.map(function(item){
        return item.name;
    });

    return selected;
}

var updateSolo = function(data){
    var copiedData = (JSON.parse(JSON.stringify(data)));
    var groupedData = groupDataByLine(copiedData);
    solo = getTopCurrentLines(groupedData);

    return solo;
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
                    currentTitleAttrs['line'] = value;
                    viz.y({
                        'label': {
                            'value': balance ? dictionary['trade_' + value] : dictionary[value]
                        }
                    });
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
                .data([{'id': 'type', 'label': dictionary['value']}, {'id': 'trade_balance', 'label': dictionary['trade_balance']}])
                .title(dictionary['depth'])
                .type('toggle')
                .focus(dictionary['value'] ? 'type' : 'trade_balance', function(value) {
                    viz.id({
                        'value' : value == 'trade_balance' ? value : [group, value]
                    });
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
                    viz.data({'value': data, 'padding': 0})
                    viz.x({
                        'value': value,
                        'label': value == 'year' ? dictionary['year'] : dictionary['month']
                    });
                    viz.time({
                        'value': value
                    })
                    viz.draw();
                })
                .draw();
        }

        // Adds logarithm selector
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

    };

    var titleHelper = function(years) {
        if (!baseTitle) {
            var genericTitle = '<line> ' + dictionary['per'] + ' <yValue>';
            if (depths.length > 1 && currentTitleAttrs['yValue'] != currentTitleAttrs['yValue'])
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
        if(balance){
            return {
                'short': {
                    '': yValues
                }
            }
        }

        return {
            'short': {
                '': ID_LABELS.hasOwnProperty(line) ? dictionary[ID_LABELS[line]] : 'id',
                '': [yValue]
            },
            'long': {
                '': ID_LABELS.hasOwnProperty(line) ? dictionary[ID_LABELS[line]] : 'id',
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
        toolsBuilder('lineGraph', viz, data, titleHelper(selectedYears).value);
        viz.title(titleHelper(selectedYears));
    };

    var viz = d3plus.viz()
        .container('#lineGraph')
        .data({'value': data, 'padding': 0})
        .type('line')
        .shape({'interpolate': 'monotone'})
        .x({
            'value': 'year',
            'ticks': {'font': {'size': 18}},
            'label': {'font': {'size': 20}}
        })
        .y({
            'value': yValue,
            'ticks': {'font': {'size': 18}},
            'label': {'font': {'size': 20}}
        })
        .axes({'background': {'color': '#FFFFFF'}})
        .background('transparent')
        .labels({'align': 'left', 'valign': 'top'})
        .time({'value': 'year', 'solo': {'callback': timelineCallback}})
        .icon({'value': 'icon', 'style': 'knockout'})
        .legend({'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleHelper(selectedYears))
        .title({'total': {'font': {'align': 'left'}}})
        .tooltip(tooltipBuilder())
        .format(formatHelper())

        if (group && group != line){
            viz.id([group, line]);
            viz.color(group);
        } else
            viz.id(line).color(line);

        if (COLORS.hasOwnProperty(group)) {
            viz.attrs(COLORS[group]);
            viz.color('color');
        } else
            viz.color({'scale':'category20', 'value': args['color'] || depths[0]});

        if (students) {
            viz.id(line).color(line);
            viz.y({'label': {'value': dictionary['students_number']}});
            viz.color({'scale':'category20', 'value': line});
        }

        if (balance)
            viz.y({'label': {'value': dictionary['trade_value']}});

        if (port)
            viz.id({'solo': solo});

    uiBuilder();
    $('#lineGraph').css('height', (window.innerHeight - $('#controls').height() - 40) + 'px');
    viz.draw();

    if ($('#controls').css('display') == 'none')
        $('#controls').fadeToggle();

    toolsBuilder('lineGraph', viz, data, titleHelper(yearRange).value);

};

var getUrls = function() {
    var dimensions = [dataset, (dataset == 'secex' ? 'month/year' : 'year'), line],
    metadataAttrs = [];

    if (students){
        dimensions.pop();
        metadataAttrs.push(group);
    } else {
        depths.concat(filters).forEach(function(attr) {
            if (attr != line && dimensions.indexOf(attr) == -1) {
                dimensions.push(attr);
                metadataAttrs.push(attr);
            }
        });
    }

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

            if (students)
                line = 'students';
            else
                data = fillMissingDates(data);

            if (balance){
                data.sort(function(a,b) {return (a['date'] > b['date']) ? 1 : ((b['date'] > a['date']) ? -1 : 0);})
                buildTradeBalanceData(data);
            }

            if (port)
                var solo = updateSolo(data);

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

:: Line Graph General Informations ::

Appears in the categories: Location, Product, Trade Partner e High Education (Major)
Data Bases usage: SECEX, HEDU
Especific conditions or variables:
    - Completes missing dates function 
    - Calculates Trade Balance variable (Exports - Imports)
    - Port variable has the function solo to filter top data
    - Students situation need to split data into specific format  

*/
