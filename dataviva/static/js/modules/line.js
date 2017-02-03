var lang = document.documentElement.lang,
    solo = [],
    data = [],
    dataset = $("#line").attr("dataset"),
    line = $("#line").attr("line"),
    options = $("#line").attr("options").split(","),
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

var textHelper = {
    'loading': {
        'en': 'loading ...',
        'pt': 'carregando ...'
    },
    'average_wage': {
        'en': 'Salário Médio Mensal',
        'pt': 'Average Monthly Wage'
    },
    'jobs': {
        'en': 'Jobs',
        'pt': 'Empregos'
    },
    'year': {
        'en': 'Year',
        'pt': 'Ano'
    },
    'scale': {
        'en': "Scale",
        'pt': "Escala"
    },
    'yaxis': {
        'en': "Y-Axis",
        'pt': "Eixo Y"
    },
    'locale': {
        'en': 'en_US',
        'pt': 'pt_BR'
    },
    'average_wage': {
        'en': "Average Monthly Wage",
        'pt': "Salário Médio Mensal"  
    },
    'kg': {
        'en': 'Amount',
        'pt': 'Quantidade'
    },
    'value': {
        'en': "Value",
        'pt': "Valor"
    },
    'kg_label': {
        'en': 'Amount [kg]',
        'pt': 'Quantidade [kg]'
    },
    'value_label': {
        'en': "Value [$ USD]",
        'pt': "Valor [$ USD]"
    },
    'average_wage_label': {
        'en': "Average Monthly Wage [$ USD]",
        'pt': "Salário Médio Mensal [$ USD]"  
    },
    'jobs_label': {
        'en': "Jobs",
        'pt': "Empregos"  
    },
    'data_provided_by': {
        'en': "Data provided by ",
        'pt': "Dados fornecidos por ",
    },
        'month': {
        'en': "Month",
        'pt': "Mês"  
    },
    'time_resolution': {
        'en': "Time Resolution",
        'pt': "Resolução Temporal"  
    }
};

var formatHelper = {
    "text": function(text, params) {
        if (textHelper[text] != undefined)
            return textHelper[text][lang];

        return d3plus.string.title(text, params);
    },

    "number": function(number, params) {
        var formatted = d3plus.number.format(number, params);

        if (params.key == "value" && number == FAKE_VALUE)
            return lang == 'en' ? "Not Available" : "Não disponível";

        if (params.key == "kg" && number == FAKE_VALUE)
            return lang == 'en' ? "Not Available" : "Não disponível";
        
        if (params.key == "value" && params.labels == undefined)
            return "$" + formatted + " USD";

        if (params.key == "kg" && params.labels == undefined)
            return formatted + " kg";

        return formatted;
    }
};

var uiHelper = {
    'scale': {
        "label": textHelper.scale[lang],
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
        'label': textHelper.yaxis[lang],
        'value': values,
        'method': function(value, viz){
            currentX = value;
            solo = updateSolo(data)
            viz.y({
                "value": value,
                "label": textHelper[value + '_label'][lang],
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
            viz.time(value).x(value).draw();
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

var loadViz = function(data){
    var visualization = d3plus.viz()
        .container("#line")
        .data(data)
        .type("line")
        .text("name")
        .id({
            'value': line,
            'solo': solo
        })
        .background("transparent")
        .shape({
            "interpolate": "monotone"
        })
        .x({
            "value": 'year',
            'label': {
                'value': textHelper.year[lang]
            }
        })
        .y({
            "value": value,
            "label": {
                "value": textHelper[value + '_label'][lang],
                "font": {
                    "size": 20
                }
            }
        })
        .format(formatHelper)
        .title(titleStyle)
        .title(title)
        .tooltip("type")
        .ui(uis)
        .footer({
            "value": textHelper["data_provided_by"][lang] + dataset.toUpperCase()
        })
        .time('year')

        if(options.indexOf('singlecolor') != -1){
            visualization.color({
                "value" : function(d){
                    return "#4d90fe";
                }
            }).legend(false)
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

var processData = function(data){

    var fillMissingDates = function(data){
        var dates = new Set();
        var lines = new Set();
        var check = {};

        data.forEach(function(item){
            dates.add(item.date);
            lines.add(item[line]);

            if(check[item[line]] == undefined)
                check[item[line]] = {};

            check[item[line]][item.date] = true;
        });

        dates = Array.from(dates);
        lines = Array.from(lines);

        dates.forEach(function(date){
            lines.forEach(function(lineValue){
                if(check[lineValue][date] == undefined){
                    var dataItem = {};
                    dataItem['date'] = date;
                    dataItem['year'] = date.split('/')[0];
                    dataItem['month'] = date.split('/')[1];
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
            item['date'] = item['year'] + '/' + item['month'];

        return item;
    });

    data = fillMissingDates(data);

    data = data.map(function(item){
        if(line_metadata[item[line]])
            item.name = line_metadata[item[line]]['name_' + lang];
        else{
            item.name = lang == 'en' ? 'Undefined': 'Não disponível';
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

var loading = dataviva.ui.loading('.loading').text(textHelper.loading[lang]);

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + line
    ], 

    function(responses){
        api = responses[0];
        line_metadata = responses[1];

        var data = buildData(api);
        data = processData(data);
        solo = updateSolo(data);

        loading.hide();
        loadViz(data);
    })
});