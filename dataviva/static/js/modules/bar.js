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

var visualization;

var uis = [];

if(x.length > 1){
    uis.push({
        'value': x,
        'type': 'drop',
        'label': 'xaxis',
        'method': function(value, viz){
            currentX = value;
            viz.x(value)
               .order({
                    'value': data[0][currentY + '_order'] == undefined ? currentX : currentY + '_order',
                    'sort': data[0][currentY + '_order'] == undefined ? 'asc' : 'desc'
                })
               totalOfCurrentX()
            viz.draw()
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
                .id(value)
                .order({
                    'value': data[0][currentY + '_order'] == undefined ? currentX : currentY + '_order',
                    'sort': data[0][currentY + '_order'] == undefined ? 'asc' : 'desc'
                })
                .draw();
        }
    });
}

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
    'xaxis': {
        'en': "X-Axis",
        'pt': "Eixo X"
    },
    'locale': {
        'en': 'en_US',
        'pt': 'pt_BR'
    },
    'average_wage': {
        'en': "Average Wage",
        'pt': "Salário Médio"  
    },
    'kg': {
        'en': 'kg',
        'pt': 'kg'
    },
    'value': {
        'en': "US$",
        'pt': "US$"
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
    'kg_pct': {
        'en': "% of kg",
        'pt': "% de kg"  
    },
    'value_pct': {
        'en': "% of US$",
        'pt': "% de US$"  
    },
    'simple': {
        'en': "Simples",
        'pt': "Simples"  
    },
    'establishment_size': {
        'en': "Establishment Size",
        'pt': "Tamanho do Estabelecimento"  
    },
    'average_establishment_size': {
        'en': "Average Establishment Size",
        'pt': "Tamanho Médio do Estabelecimento"  
    },
    'establishment_count': {
        'en': "Establishments",
        'pt': "Estabelecimentos"  
    },
    'wage': {
        'en': "Salary Mass",
        'pt': "Massa Salarial"   
    },
    'gender': {
        'en': "Gender",
        'pt': "Gênero"  
    },
    'ethnicity': {
        'en': "Ethnicity",
        'pt': "Etnia"  
    },
    'literacy': {
        'en': "Literacy",
        'pt': "Escolaridade"  
    },
    'month': {
        'en': "Month",
        'pt': "Mês"  
    },
    'port': {
        'en': "Port",
        'pt': "Porto"  
    },
    'legal_nature': {
        'en': "Legal Nature",
        'pt': "Natureza Jurídica"  
    },
    'size_establishment': {
        'en': "Establishment Size ",
        'pt': "Tamanho do Estabelecimento"  
    },
    'time_resolution': {
        'en': "Time Resolution",
        'pt': "Resolução Temporal"  
    },
    'total_of': {
        'en': "Total in selected years: ",
        'pt': "Total nos anos selecionados: ",
    },
    'data_provided_by': {
        'en': "Data provided by ",
        'pt': "Dados fornecidos por ",
    }
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

        if (textHelper[text] != undefined)
            return textHelper[text][lang];

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
     visualization = d3plus.viz()
        .container("#bar")
        .data(data)
        .background("transparent")
        .type("bar")
        .font({
            'size': 13
        })
        .id({
            'value': currentY,
            'solo': solo
        })
        .y({
            "value": currentY,
            "scale": "discrete",
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
                'callback': totalOfCurrentX
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
            "value": textHelper["data_provided_by"][lang] + dataset.toUpperCase()
        })


        if(options.indexOf('singlecolor') != -1){
            visualization.color({
                "value" : function(d){
                    return "#4d90fe";
                }
            }).legend(false)
        }
        totalOfCurrentX();
        visualization.draw()
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
            'value': textHelper["total_of"][lang] + formatHelper.number(total, {key: key}),
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

    x.forEach(function(xValue){
        x.push(xValue + '_pct')
    });

    return data;
}

var addNameToData = function(data){
    y.forEach(function(itemY){
        data = data.map(function(item){
            if(metadatas[itemY][item[itemY]] == undefined){
                item[itemY] = 'NOT FOUND!';
            }
            else{
                item[itemY] = metadatas[itemY][item[itemY]]['name_' + lang];
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

var lastYear = function(data){
    var year = 0;

    data.forEach(function(item){
        if(item.year > year)
            year = item.year;
    });

    return year;
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
            data = addOrder(data);
            data = addNameToData(data);
            data = addPercentage(data);
            solo = updateSolo(data);

            loading.hide();
            loadViz(data);
        }
    );
});