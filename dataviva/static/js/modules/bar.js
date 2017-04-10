var unique = function(item, i, arr){ 
    return arr.indexOf(item) == i;
}

var data = [],
    MAX_BARS = 10,
    currentFilters = {},
    lang = document.documentElement.lang,
    dataset = $("#bar").attr("dataset"),
    subtitle = $("#bar").attr("subtitle"),
    options = $("#bar").attr("options").split(","),
    x = $("#bar").attr("x").split(","),
    currentX = x[0],
    y = $("#bar").attr("y").split(","),
    currentY = y[0],
    vizId = getUrlArgs()['id'] ? getUrlArgs()['id'] : undefined,
    filters = $("#bar").attr("filters"),
    baseTitle = $("#bar").attr('graph-title'),
    baseSubtitle = $("#bar").attr('graph-subtitle'),
    uiFilters = getUrlArgs().filters ? getUrlArgs().filters.split(',') : [],
    dimensions = y.concat(uiFilters).filter(unique),
    dimensions = vizId ? dimensions.concat(vizId).filter(unique) : dimensions,
    dimensions = options.indexOf('attention_level') != -1 ? dimensions.concat(['ambulatory_attention', 'hospital_attention']).filter(unique) : dimensions,
    yearRange = [Number.POSITIVE_INFINITY, 0],
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + (options.indexOf('month') != -1 ? 'month/' : '') + dimensions.join("/") + ( filters ? "?" + filters : '');


var currentTitleAttrs = {'shapes': y[0]}

var visualization;
var percentage = false;

var uis = [];

var titleHelper = function(years) {
    var header = titleBuilder(baseTitle, baseSubtitle, currentTitleAttrs, dataset, getUrlArgs(), years);

    return {
        'value': header['title'],
        'font': {'size': 22, 'align': 'left'},
        'padding': 5,
        'sub': {'font': {'align': 'left'}, 'value': header['subtitle']},
        'width': window.innerWidth - d3.select('#tools').node().offsetWidth - 20
    };
};

if(x.length > 1){
    uis.push({
        'value': x,
        'type': 'drop',
        'label': 'xaxis',
        'method': function(value, viz){
            currentX = value;

            if(percentage)
                currentX = currentX + '_pct';

            viz.x(currentX)
               .order({
                    'value': data[0][currentY + '_order'] == undefined ? currentX : currentY + '_order',
                    'sort': data[0][currentY + '_order'] == undefined ? 'asc' : 'desc'
                })
            totalOfCurrentX();
            viz.draw();
        }
    });
}

if(y.length > 1){
    uis.push({
        'value': y,
        'type': 'drop',
        'label': 'yaxis',
        'method': function(value, viz){
            currentY = value;

            viz.y(value)
                .id(vizId ? vizId : value)
                .order({
                    'value': data[0][currentY + '_order'] == undefined ? currentX : currentY + '_order',
                    'sort': data[0][currentY + '_order'] == undefined ? 'asc' : 'desc'
                })
                .legend(false)

            if(colorHelper[currentY] != undefined)
                viz.color(currentY + "_color");

            currentTitleAttrs['shapes'] = value;

            viz.title(titleHelper(yearRange))
                .data(filterTopData(data))
                .draw();
        }
    });
}

var colorHelper = {
   'gender': {
        '0': '#d73027',
        '1': '#4575b4'
   },
   'literacy': {
        '-1':'#d73027',
        '1':'#f46d43',
        '2':'#fdae61',
        '3':'#fee090',
        '4':'#e0f3f8',
        '5':'#abd9e9',
        '6':'#74add1',
        '7':'#4575b4'
   },
   'ethnicity': {
        '-1': '#f46d43',
        '1': '#fdae61',
        '2': '#fee090',
        '4': '#e0f3f8',
        '6': '#abd9e9',
        '8': '#74add1'
   },
   'simple': {
        '0': '#f46d43',
        '1': '#74add1' 
   },
   'establishment_size': {
        '-1': '#d73027',
        '0': '#f46d43',
        '1': '#fdae61',
        '2': '#abd9e9',
        '3': '#74add1',
        '4': '#4575b4'
   },
   'legal_nature': {
        '-1':'#d73027',
        '1':'#f46d43',
        '2':'#fdae61',
        '3':'#fee090',
        '4':'#e0f3f8',
        '5':'#abd9e9',
        '6':'#74add1',
        '7':'#4575b4'
    }
}

var addColor = function(data){
   data = data.map(function(item){
       for(key in colorHelper){
           if(item[key] != undefined)
               item[key + '_color'] = colorHelper[key][item[key]];
       }

       return item;
   });

   return data;
};

var orderHelper = {
    'ethnicity': {
        '-1': 6,
        '1': 5,
        '2': 1,
        '4': 3,
        '6': 4,
        '8': 2
    },
    'gender': {
        '0': 2,
        '1': 1
    },
    'literacy': {
        '-1': 8,
        '1': 7,
        '2': 6,
        '3': 5,
        '4': 4,
        '5': 3,
        '6': 2,
        '7': 1
    },
    'simple': {
        '0': 2,
        '1': 1 
    },
    'establishment_size': {
        '-1': 5,
        '0': 6,
        '1': 4,
        '2': 3,
        '3': 2,
        '4': 1
    },
    'legal_nature': {
        '-1': 8,
        '1': 1,
        '2': 2,
        '3': 3,
        '4': 4,
        '5': 5,
        '6': 6,
        '7': 7
    }
}

var addUiFilters = function(){
    var config = {
        'id': 'id',
        'text': 'label',
        'font': {'size': 11},
        'container': d3.select('#controls'),
        'search': false
    };

    var filteredData = function(data, filter, value) {
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

    uiFilters.forEach(function(filter, j) {
        currentFilters[filter] = -1;
        var options = [];
        for (id in metadatas[filter]) {
            options.push({'id': metadatas[filter][id]['name_' + lang], 'label': metadatas[filter][id]['name_' + lang]})
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
                var filtered = filteredData(data, filter, value);
                filtered = filterTopData(filtered);
                visualization.data(filtered);
                visualization.draw();
            })
            .draw();
    });

    // Custom filter to Attention Level
    // To use, add: options=attention_level
    if(options.indexOf('attention_level') != -1) {

        currentFilters['ambulatory_attention'] = -1;
        currentFilters['hospital_attention'] = -1;

        var filterValues = [
            [-1, -1], // Todos 
            [metadatas['ambulatory_attention'][0]['name_' + lang], metadatas['hospital_attention'][0]['name_' + lang]],   // Nenhum
            [metadatas['ambulatory_attention'][0]['name_' + lang], metadatas['hospital_attention'][1]['name_' + lang]],   // Hospitalar
            [metadatas['ambulatory_attention'][1]['name_' + lang], metadatas['hospital_attention'][0]['name_' + lang]],   // Ambulatorial
            [metadatas['ambulatory_attention'][1]['name_' + lang], metadatas['hospital_attention'][1]['name_' + lang]]    // Ambulatorial/Hospitalar
        ];

        var menuOptions = [
            {
                id: 0,
                label: dictionary['all']
            },
            {
                id: 1,
                label: dictionary['none']
            },
            {
                id: 2,
                label: dictionary['hospital']
            },
            {
                id: 3,
                label: dictionary['ambulatory']
            },
            {
                id: 4,
                label: dictionary['ambulatory/hospital']
            },
        ];

        d3plus.form()
            .config(config)
            .container(d3.select('#controls'))
            .data(menuOptions)
            .title('Nível de Atenção')
            .type('drop')
            .font({'size': 11})
            .focus(-1, function(pos) {
                var filtered = filteredData(data, 'ambulatory_attention', filterValues[pos][0]);
                filtered = filteredData(data, 'hospital_attention', filterValues[pos][1]);
                filtered = filterTopData(filtered);
                visualization.data(filtered).draw();
            })
            .draw();
    }
};

var addOrder = function(data){
    data = data.map(function(item){
        for(key in orderHelper){
            if(item[key] != undefined)
                item[key + '_order'] = orderHelper[key][item[key]];
        }

        return item;
    });

    return data;
};

var formatNumber = function(digit){
    var lastDigit = digit.slice(-1);

    if(!isNaN(lastDigit))
        return digit;

    var number =  digit.slice(0, -1);

    var scale = {
        'T': {
            'en': number < 2 ? ' Trillion' : ' Trillions',
            'pt': number < 2 ? ' Trilhão' : ' Trilhões'
        },
        'B': {
            'en': number < 2 ? ' Billion' : ' Billions',
            'pt': number < 2 ? ' Bilhão' : ' Bilhões'
        },
        'M': {
            'en': number < 2 ? ' Million' : ' Millions',
            'pt': number < 2 ? ' Milhão' : ' Milhões'
        },
        'k': {
            'en': ' Thousand',
            'pt': ' Mil'
        }
    }
    return number + scale[lastDigit][lang];
}


var formatHelper = {
    "text": function(text, params) {
        if(params.labels == false)
            return text;

        if (dictionary[text] != undefined)
            return dictionary[text];

        return d3plus.string.title(text, params); 
    },

    "number": function(number, params) {
        var formatted = d3plus.number.format(number, params);

        formatted = formatNumber(formatted)
        
        if (params.key == "value" && params.labels == undefined)
            return "$" + formatted + " USD";

        if (params.key == "kg" && params.labels == undefined)
            return formatted + " kg";

        if (params.key == "wage" && params.labels == undefined)
            return "$" + formatted + " BRL";

        if (params.key == "average_wage" && params.labels == undefined)
            return "$" + formatted + " BRL";

        if (params.key == "kg_pct" && params.labels == undefined)
            return parseFloat(formatted).toFixed(1) + "%";

        if (params.key == "value_pct" && params.labels == undefined)
            return parseFloat(formatted).toFixed(1) + "%";

        return formatted;
    }
};

var loadViz = function(data){
    var timelineCallback = function(years) {
        var selectedYears = [];
        if (!years.length)
            selectedYears = yearRange;
        else if (years.length == 1)
            selectedYears = [0, years[0].getFullYear()];
        else
            selectedYears = [years[0].getFullYear(), years[years.length - 1].getFullYear()]
        toolsBuilder('bar', visualization, data, titleHelper(selectedYears).value);
        visualization.title(titleHelper(selectedYears));
        totalOfCurrentX(years);
    };

    visualization = d3plus.viz()
        .container("#bar")
        .data(data)
        .background("transparent")
        .type("bar")
        .height(window.innerHeight - $('#controls').height() - 40)
        .font({
            'size': 13
        })
        .id({
            'value': vizId ? vizId : currentY,
        })
        .y({
            "value": currentY,
            "scale": "discrete",
            'grid': false,
            'label': {
                'font': {
                    'size': 22
                }
            }
        })
        .x({
            "value": currentX,
            'label': {
                'font': {
                    'size': 16
                }
            }
        })
        .ui(uis)
        .format(formatHelper)
        .time({
            'value': 'year',
            'solo': {
                'value': [lastYear(data)],
                'callback': timelineCallback
            }
        })
        .aggs({
            'average_wage': 'mean',
            'ethnicity_order': 'mean',
            'gender_order': 'mean',
            'literacy_order': 'mean',
            'simple_order': 'mean',
            'establishment_size_order': 'mean',
            'legal_nature_order': 'mean'
        })
        .order({
            'value': data[0][currentY + '_order'] == undefined ? currentX : currentY + '_order',
            'sort': data[0][currentY + '_order'] == undefined ? 'asc' : 'desc'
        })
        .footer({
            "value": dictionary["data_provided_by"] + (dictionary[dataset] || dataset).toUpperCase()
        })
        .color(vizId)
        .messages({'branding': true, 'style': 'large'})
        .title(titleHelper([0, yearRange[1]]))

        if(colorHelper[currentY] != undefined)
            visualization.color(currentY + "_color");

        if(options.indexOf('nolabely') != -1){
            visualization.y({
                'label': false
            })
        }

        if(options.indexOf('singlecolor') != -1){
            visualization.color({
                "value" : function(d){
                    return "#4575b4";
                }
            }).legend(false)
        }
        totalOfCurrentX();
        visualization.draw()

        toolsBuilder('bar', visualization, data, titleHelper(yearRange));
};

var getSelectedYears = function() {
    var years = $('#timeline #labels [fill="rgba(68,68,68,1)"]').map(function (index, item){
        return +item.innerHTML
    })

    years = Array.from(years);
    years = years.filter(function(item){
        return item > 0;
    });
    return years;
}

var totalOfCurrentX = function(){
    var years = getSelectedYears();
    years = years.length == 0 ? [lastYear(data)] : years;

    var key = currentX.endsWith('_pct') ? currentX.slice(0, currentX.indexOf('_pct')) : currentX;
    var total = data.reduce(function(acc, item){
        if(years.indexOf(item.year) != -1){
            acc += item[key];
        }
        return acc;
    }, 0);

    visualization.title({
        'sub': {
            'value': dictionary["total_of"] + formatHelper.number(total, {key: key}) + (subtitle ? ' - ' + dictionary[subtitle] : ''),
            'font': {
                'align': 'left'
            }
        }
    })
};

var buildData = function(responseApi){

    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = responseApi.headers;

    responseApi.data.forEach(function(item){
        var dataItem = {};

        headers.forEach(function(header){
            dataItem[header] = getAttrByName(item, header);
        });

        if (dataItem.hasOwnProperty('year') && dataItem['year'] > yearRange[1])
            yearRange[1] = dataItem['year'];
        else if (dataItem.hasOwnProperty('year') && dataItem['year'] < yearRange[0])
            yearRange[0] = dataItem['year'];

        data.push(dataItem);
    });

    return data;
}

var addPercentage = function(data){
    if(options.indexOf('percentage') == -1)
        return data;

    var groupBy = options.indexOf('month') != -1 ? 'date' : 'year';

    var total = {};

    data.forEach(function(item){
        x.forEach(function(xValue){
            if(total[xValue] == undefined)
                total[xValue] = {};

            if(total[xValue][item.year] == undefined)
                total[xValue][item.year] = 0;

            total[xValue][item.year] += item[xValue];
        });
    });

    data = data.map(function(item){
        x.forEach(function(xValue){
            item[xValue + '_pct'] = 100 * (item[xValue] / total[xValue][item.year]);
        });

        return item;
    });

    uis.unshift({
        'value': ['values', 'percentage_terms'],
        'type': 'drop',
        'label': 'Layout',
        'method': function(value, viz){
            percentage = value == 'percentage_terms' ? true : false;

            if(currentX.indexOf( "_pct" ) != -1)
                currentX = currentX.slice(0, -4);

            if(percentage)
                currentX = currentX + '_pct';

            viz.x(currentX).draw()
            totalOfCurrentX()
        }
    })

    return data;
}

var addNameToData = function(data){
    dimensions.forEach(function(dimension){
        data = data.map(function(item){
            if(metadatas[dimension][item[dimension]] == undefined){
                item[dimension] = 'NOT FOUND!';
            }
            else{
                item[dimension] = metadatas[dimension][item[dimension]]['name_' + lang];
            }

            return item;
        });
    });

    data = data.map(function(item){
        if(item['wage'] != undefined)
            item['wage'] = +item['wage'];

        if(item['average_wage'] != undefined)
            item['average_wage'] = +item['average_wage'];

        if(item['month'] != undefined)
            item['date'] = item['year'] + '/' + item['month'];

        return item;
    });

    if(options.indexOf('month') != -1){
        uis.push({
            'method': 'time',
            'label': 'time_resolution',
            'value': [
                {'month': 'date'},
                {'year': 'year'}
            ]
        });
    }

    return data;
};

var filterTopData = function(data){
    var items = {}; // name: totalValue

    data.forEach(function(item){
        var name = item[currentY],
            value = item[currentX];

        if(items[name] == undefined)
            items[name] = 0;

        items[name] += value;
    });

    var sortable = [];
    for (var name in items) {
        sortable.push([name, items[name]]);
    }

    sortable.sort(function(a, b) {
        return b[1] - a[1];
    });

    var tops = sortable.splice(0, MAX_BARS);
    tops = tops.map(function(item){return item[0]})

    var binaryVariables = ['emergency_facility', 'ambulatory_care_facility', 'surgery_center_facility', 'obstetrical_center_facility', 'neonatal_unit_facility']

    if(binaryVariables.indexOf(currentY) != -1){
        tops = [metadatas[currentY][1]['name_' + lang]];
    }

    return data.filter(function(item){
        return tops.indexOf(item[currentY]) != -1;
    });
}


var lastYear = function(data){
    var year = 0;

    data.forEach(function(item){
        if(item.year > year)
            year = item.year;
    });

    return year;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization'] + '...');

$(document).ready(function(){
    var urls = [url];

    dimensions.forEach(function(item){
        urls.push("http://api.staging.dataviva.info/metadata/" + item);
    });

    ajaxQueue(
        urls, 
        function(responses){
            api = responses.shift();
            metadatas = {};

            dimensions.forEach(function(item, index){
                metadatas[item] = responses[index];
            });

            data = buildData(api);
            data = addColor(data);
            data = addOrder(data);
            data = addNameToData(data);
            data = addPercentage(data);

            addUiFilters();

            loading.hide();
            d3.select('#mask').remove();
            loadViz(filterTopData(data));
        }
    );
});
