var data = [],
    solo = [],
    MAX_BARS = 10,
    lang = document.documentElement.lang,
    dataset = $("#bar").attr("dataset"),
    options = $("#bar").attr("options").split(","),
    x = $("#bar").attr("x").split(","),
    currentX = x[0],
    y = $("#bar").attr("y").split(","),
    currentY = y[0],
    filters = $("#bar").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + ( options.indexOf('month') != -1 ? 'month/' : '' ) + y.join("/") + ( filters ? "?" + filters : '');


// TODO: Title creator
var title = 'Title';
var textHelper = {
    'loading': {
        'en': 'loading ...',
        'pt': 'carregando ...'
    }
};

var visualization;

var uis = [
    {
        'method': 'x',
        'value': x,
        'type': 'drop'
    },
    {
        'value': y,
        'type': 'drop',
        'method': function(value, viz){
            viz.y(value).id(value).draw();
        }
    }
];

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
    'xaxis': {
        'en': "X-Axis",
        'pt': "Eixo X"
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
    },
    'kg_pct': {
        'en': "% de kg",
        'pt': "% of kg"  
    },
    'value_pct': {
        'en': "% de US$",
        'pt': "% of US$"  
    },
    'simples': {
        'en': "Simples",
        'pt': "Simples"  
    },
    'establishment_size': {
        'en': "Establishment Size",
        'pt': "Tamanho do Estabelecimento"  
    },
    'wage_received': {
        'en': "Wage Received",
        'pt': "Salário Recebido"  
    },
    'gender': {
        'en': "Gender",
        'pt': "Salário Recebido"  
    },
    'ethnicity': {
        'en': "Ethnicity",
        'pt': "Etnia"  
    },
    'literacy': {
        'en': "Literacy",
        'pt': "Escolaridade"  
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
        
        if (params.key == "value" && params.labels == undefined)
            return "$" + formatted + " USD";

        if (params.key == "kg" && params.labels == undefined)
            return formatted + " kg";

        if (params.key == "kg_pct" && params.labels == undefined)
            return parseFloat(formatted * 100).toFixed(1) + "%";

        if (params.key == "value_pct" && params.labels == undefined)
            return parseFloat(formatted * 100).toFixed(1) + "%";

        return formatted;
    }
};

var loadViz = function(data){
     visualization = d3plus.viz()
        .container("#bar")
        .data(data)
        .background("transparent")
        .type("bar")
        .id({
            'value': currentY,
            'solo': solo
        })
        .y({
            "value": currentY,
            "scale": "discrete" // Manually set Y-axis to be discrete
        })
        .x(currentX)
        .ui(uis)
        .format(formatHelper    )
        .time('year')
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
            item[xValue + '_pct'] = item[xValue] / total[xValue][item.year];
        });

        return item;
    });

    x.forEach(function(xValue){
        x.push(xValue + '_pct')
    });

    return data;
}

var addNameToData = function(data){
    y.forEach(function(itemY){
        data = data.map(function(item){
            if(metadatas[itemY][item[itemY]] == undefined){
                // console.log("Not found name to: " + itemY + ' - ' + item[itemY]);
                item[itemY] = 'NOT FOUND!';
            }
            else{
                item[itemY] = metadatas[itemY][item[itemY]]['name_' + lang];
            }


            return item;
        });
    });

    data = data.map(function(item){
        if(item['wage_received'] != undefined)
            item['wage_received'] = +item['wage_received'];

        if(item['average_monthly_wage'] != undefined)
            item['average_monthly_wage'] = +item['average_monthly_wage'];

        if(item['month'] != undefined)
            item['date'] = item['year'] + '/' + item['month'];

        return item;
    });

    if(options.indexOf('month') != -1){
        uis.push({
            'method': 'time',
            'value': [
                {'month': 'date'},
                {'year': 'year'}
            ]
        });
    }

    return data;
};

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

var loading = dataviva.ui.loading('.loading').text(textHelper.loading[lang]);

$(document).ready(function(){
    var urls = [url];

    y.forEach(function(item){
        urls.push("http://api.staging.dataviva.info/metadata/" + item);
    });

    ajaxQueue(
        urls, 
        function(responses){
            api = responses.shift();
            metadatas = {};

            y.forEach(function(item, index){
                metadatas[item] = responses[index];
            });

            data = buildData(api);
            data = addNameToData(data);
            data = addPercentage(data);
            solo = updateSolo(data);

            loading.hide();
            loadViz(data);
        }
    );
});