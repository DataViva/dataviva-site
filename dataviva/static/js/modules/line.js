var lang = document.documentElement.lang,
    solo = [],
    data = [],
    dataset = $("#line").attr("dataset"),
    line = $("#line").attr("line"),
    options = $("#line").attr("options").split(","),
    subtitle = $("#line").attr("subtitle"),
    filters = $("#line").attr("filters"),
    values = $("#line").attr("values").split(','),
    value = values[0],
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + ( options.indexOf('month') != -1 ? 'month/' : '' ) + line + ( filters ? "?" + filters : '');

var titleHelper = {
    'import': {
        'en': 'Importation of ',
        'pt': 'Importação de '
    },
    'export': {
        'en': 'Exportation of ',
        'pt': 'Exportação de '
    },
    'port': {
        'en': ' by port',
        'pt': ' por porto'
    }
};

// TODO: Title creator
var title = 'Title';

if(window.parent.document.querySelector('h1')){
    var pageTitle = window.parent.document.querySelector('h1').childNodes[0].textContent.replace(/\s+/g,' ').trim();
    title = titleHelper[type][lang] + pageTitle + titleHelper.port[lang];
}


var titleStyle = {
    "font": {
        "align": "left",
        "size": 22,
        "color": '#888'
    },
    "padding": 5,
    "sub": {
        "font": {
            "align": "left"
        }
    },
    "total": {
        "font": {
            "align": "left"
        }
    }
}

var dictionary = {};

dictionary['loading'] = lang ==  'en' ? 'loading ...' : 'carregando ...';
dictionary['average_wage'] = lang ==  'en' ? 'Salário Médio Mensal' : 'Average Monthly Wage';
dictionary['jobs'] = lang ==  'en' ? 'Jobs' : 'Empregos';
dictionary['year'] = lang ==  'en' ? 'Year' : 'Ano';
dictionary['scale'] = lang ==  'en' ? "Scale" : "Escala";
dictionary['yaxis'] = lang ==  'en' ? "Y-Axis" : "Eixo Y";
dictionary['locale'] = lang ==  'en' ? 'en_US' : 'pt_BR';
dictionary['average_wage'] = lang ==  'en' ? "Average Monthly Wage" : "Salário Médio Mensal"  ;
dictionary['kg'] = lang ==  'en' ? 'Amount' : 'Quantidade';
dictionary['value'] = lang ==  'en' ? "Value" : "Valor";
dictionary['kg_label'] = lang ==  'en' ? 'Amount [kg]' : 'Quantidade [kg]';
dictionary['value_label'] = lang ==  'en' ? "Value [$ USD]" : "Valor [$ USD]";
dictionary['average_wage_label'] = lang ==  'en' ? "Average Monthly Wage [$ USD]" : "Salário Médio Mensal [$ USD]"  ;
dictionary['jobs_label'] = lang ==  'en' ? "Jobs" : "Empregos"  ;
dictionary['data_provided_by'] = lang ==  'en' ? "Data provided by " : "Dados fornecidos por ";
dictionary['month'] = lang ==  'en' ? "Month" : "Mês"  ;
dictionary['time_resolution'] = lang ==  'en' ? "Time Resolution" : "Resolução Temporal"  ;
dictionary['exporting_municipality'] = lang ==  'en' ? "Based on the Exporting Municipality" : "Baseado nos Municípios Exportadores" ;
dictionary['state_production'] = lang ==  'en' ? "Based on State Production" : "Baseado nos Estados Produtores";

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
        if (dictionary[text] != undefined)
            return dictionary[text];

        return d3plus.string.title(text, params);
    },

    "number": function(number, params) {
        var formatted = d3plus.number.format(number, params);

        formatted = formatNumber(formatted)

        if (params.key == "value" && number == FAKE_VALUE)
            return lang == 'en'? "Not Available" : "Não disponível";

        if (params.key == "kg" && number == FAKE_VALUE)
            return lang == 'en'? "Not Available" : "Não disponível";
        
        if (params.key == "value" && params.labels == undefined)
            return "$" + formatted + " USD";

        if (params.key == "kg" && params.labels == undefined)
            return formatted + " kg";

        return formatted;
    }
};

var uiHelper = {
    'scale': {
        "label": dictionary.scale,
        "type": "drop",
        "value": [
            {
                "Linear": "linear"
            },
            {
                "Log": "log"
            }
        ],

        "method": function(value, viz){
            viz.y({
                "scale": value
            })
            .draw();
        }
    },
    'yaxis': {
        'label': dictionary.yaxis,
        'value': values,
        'method': function(value, viz){
            currentX = value;
            solo = updateSolo(data)
            viz.y({
                "value": value,
                "label": dictionary[value + '_label'],
            }).id({
                'solo': solo
            })
            .draw();
        }
    },
    'time_resolution': {
        'label': 'time_resolution',
        'value': [
            {'year': 'year'},
            {'month': 'date'}
        ],
        'method': function(value, viz){
            viz.time(value)
                .x(value)
                .draw();
        }
    }
};
var uis = [
    uiHelper.scale,
    uiHelper.yaxis
];

if(options.indexOf('month') != -1){
    uis.push(uiHelper.time_resolution);
}

var currentY = line;
var currentX = value;
var MAX_BARS = 10;

var groupDataByCurrentY = function(data){
    var sumByItem = {};

    data.forEach(function(item){
        if(sumByItem[item[currentY]] == undefined)
            sumByItem[item[currentY]] = {
                "sum": 0,
                "name": item[currentY]
            };

        sumByItem[item[currentY]].sum += item[currentX];
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

var getTopCurrentYNames = function(groupedData){
    var compare = function(a, b){
        if(a.sum < b.sum)
            return 1;
        if(a.sum > b.sum)
            return -1;

        return 0;
    }

    var list = groupedData.sort(compare).slice(0, MAX_BARS);

    var selected = list.map(function(item){
        return item.name;
    });

    return selected;
}

var updateSolo = function(data){
    var copiedData = (JSON.parse(JSON.stringify(data)));
    var groupedData = groupDataByCurrentY(copiedData);
    solo = getTopCurrentYNames(groupedData);

    return solo;
};

var visualization;

var loadViz = function(data){
    visualization = d3plus.viz()
        .container("#line")
        .data(data)
        .type("line")
        .text("name")
        .id({
            'value': line,
            'solo': solo
        })
        .background("transparent")
        .font({
            'size': 13
        })
        .shape({
            "interpolate": "monotone"
        })
        .x({
            "value": 'year',
            'label': {
                'value': dictionary.year,
                'font': {
                    'size': 16
                }     
            }
        })
        .y({
            "value": value,
            "label": {
                "value": dictionary[value + '_label'],
                "font": {
                    "size": 22
                }
            }
        })

        .format(formatHelper)
        .title(titleStyle)
        .title(title)
        .tooltip("type")
        .ui(uis)
        .footer({
            "value": dictionary["data_provided_by"] + dataset.toUpperCase()
        })
        .time('year')

        if(options.indexOf('singlecolor') != -1){
            visualization.color({
                "value" : function(d){
                    return "#4d90fe";
                }
            }).legend(false)
        }

        if(subtitle != ""){
            visualization.title({
                'sub': {
                    'value': dictionary[subtitle],
                    'font': {
                        'align': 'left'
                    }
                }
            })
        }

        visualization.draw()
};

var buildData = function(responseApi){

    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var headers = responseApi.headers;

    responseApi.data.forEach(function(item){
        var dataItem = {};

        headers.forEach(function(header){
            dataItem[header] = getAttrByName(item, header);
        });

        data.push(dataItem);
    });

    return data;
}

var FAKE_VALUE = 1;

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

var processData = function(data){

    var allDates = function(minYear, maxYear){
        var dates = [];
            var months = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11];
                for(var year = minYear; year <= maxYear; year++){
                    months.forEach(function(month){
                        dates.push(new Date(year, month));
                    })
                }

    return dates;
};

var fillMissingDates = function(data){
        var lines = new Set();
        var check = {};
  
        data.forEach(function(item){
            lines.add(item[line]);

            if(check[item[line]] == undefined)
                check[item[line]] = {};

            check[item[line]][item.date] = true;
        });

        var dates = allDates(firstYear(data), lastYear(data));
        lines = Array.from(lines);

        dates.forEach(function(date){
            lines.forEach(function(lineValue){
                if(check[lineValue][date] == undefined){
                    var dataItem = {};
                    dataItem['date'] = date;
                    dataItem['year'] = date.getFullYear();
                    dataItem['month'] = date.getMonth() + 1;
                    dataItem[line] = lineValue;

                    values.forEach(function(value){
                        dataItem[value] = FAKE_VALUE; // The values are setted as 1 because the logarithmic scale on the d3plus line chart does not work when the data has more than one value equal to 0.
                    });

                    data.push(dataItem);
                }
            });
        });

        return data;
    };

    data = data.map(function(item){
        if(item['month'] != undefined)
            item['date'] = new Date(item['year'], item['month'] - 1);

        return item;
    });

    data = fillMissingDates(data);

    data = data.map(function(item){
        if(line_metadata[item[line]])
            item.name = line_metadata[item[line]]['name_' + lang];
        else{
            item.name = lang == 'en'? 'Undefined': 'Não disponível';
            console.log(item[line])
        }

        return item;
    });

    data = data.map(function(item){
        if(item['average_wage'])
            item['average_wage'] = +item['average_wage'];
        
        if(item['wage'])
            item['wage'] = +item['wage'];

        return item;
    });

    return data;
}

var loading = dataviva.ui.loading('.loading').text(dictionary.loading);

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + line
    ], 

    function(responses){
        api = responses[0];
        line_metadata = responses[1];

        data = buildData(api);
        data = processData(data);
        solo = updateSolo(data);

        loading.hide();
        loadViz(data);
    })
});