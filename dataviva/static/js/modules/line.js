var lang = document.documentElement.lang,
    dataset = $("#line").attr("dataset"),
    line = $("#line").attr("line"),
    filters = $("#line").attr("filters"),
    values = $("#line").attr("values").split(','),
    value = values[0],
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + line + ( filters ? "?" + filters : '');

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
var pageTitle = window.parent.document.querySelector('h1').childNodes[0].textContent.replace(/\s+/g,' ').trim();
var title = titleHelper[type][lang] + pageTitle + titleHelper.port[lang];

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
    'average_monthly_wage': {
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
    'average_monthly_wage': {
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
    'average_monthly_wage_label': {
        'en': "Average Monthly Wage [$ USD]",
        'pt': "Salário Médio Mensal [$ USD]"  
    },
    'jobs_label': {
        'en': "Jobs",
        'pt': "Empregos"  
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
            viz.y({
                "value": value,
                "label": textHelper[value + '_label'][lang]
            }).draw();
        }
    }
};

var loadViz = function(data){
    var visualization = d3plus.viz()
        .container("#line")
        .data(data)
        .type("line")
        .text("name")
        .id(line)
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
        .ui([
            uiHelper.scale,
            uiHelper.yaxis
        ])
        .time(textHelper.year[lang])
        .draw()
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

        data.push(dataItem);
    });

    return data;
}

var FAKE_VALUE = 1;

var processData = function(data){

    var fillMissingYears = function(data){
        var years = new Set();
        var lines = new Set();
        var check = {};

        data.forEach(function(item){
            years.add(item.year);
            lines.add(item[line]);

            if(check[item[line]] == undefined)
                check[item[line]] = {};

            check[item[line]][item.year] = true;
        });

        years = Array.from(years);
        lines = Array.from(lines);

        years.forEach(function(year){
            lines.forEach(function(lineValue){
                if(check[lineValue][year] == undefined){
                    var dataItem = {};
                    dataItem['year'] = year;
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

    data = fillMissingYears(data);

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
        item['average_monthly_wage'] = +item['average_monthly_wage'];
        item['wage_received'] = +item['wage_received'];

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

        loading.hide();
        loadViz(data);
    })
});