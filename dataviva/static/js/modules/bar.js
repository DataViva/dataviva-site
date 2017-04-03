var data = [],
    solo = [],
    MAX_BARS = 10,
    lang = document.documentElement.lang,
    dataset = $("#bar").attr("dataset"),
    subtitle = $("#bar").attr("subtitle"),
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
var percentage = false;

var uis = [];

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
                .legend(false)

            if(colorHelper[currentY] != undefined)
                viz.color(currentY + "_color");

            solo = updateSolo(data);

            viz.id({
                'solo': solo,
            })
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

var dictionary = {};

dictionary['loading'] = lang == 'en' ? 'loading ...' : 'carregando ...';
dictionary['average_wage'] = lang == 'en' ? 'Salário Médio Mensal' : 'Average Monthly Wage';
dictionary['jobs'] = lang == 'en' ? 'Jobs' : 'Empregos';
dictionary['year'] = lang == 'en' ? 'Year' : 'Ano';
dictionary['scale'] = lang == 'en' ? "Scale" : "Escala";
dictionary['yaxis'] = lang == 'en' ? "Y-Axis" : "Eixo Y";
dictionary['xaxis'] = lang == 'en' ? "X-Axis" : "Eixo X";
dictionary['locale'] = lang == 'en' ? 'en_US' : 'pt_BR';
dictionary['average_wage'] = lang == 'en' ? "Average Wage" : "Salário Médio";
dictionary['kg'] = lang == 'en' ? 'kg' : 'kg';
dictionary['value'] = lang == 'en' ? "US$" : "US$";
dictionary['kg_label'] = lang == 'en' ? 'Amount [kg]' : 'Quantidade [kg]';
dictionary['value_label'] = lang == 'en' ? "Value [$ USD]" : "Valor [$ USD]";
dictionary['average_wage_label'] = lang == 'en' ? "Average Monthly Wage [$ USD]" : "Salário Médio Mensal [$ USD]";
dictionary['jobs_label'] = lang == 'en' ? "Jobs" : "Empregos";
dictionary['kg_pct'] = lang == 'en' ? "% of kg" : "% de kg";
dictionary['value_pct'] = lang == 'en' ? "% of US$" : "% de US$";
dictionary['simple'] = lang == 'en' ? "Simples" : "Simples";
dictionary['establishment_size'] = lang == 'en' ? "Establishment Size" : "Tamanho do Estabelecimento";
dictionary['average_establishment_size'] = lang == 'en' ? "Average Establishment Size" : "Tamanho Médio do Estabelecimento";
dictionary['establishment_count'] = lang == 'en' ? "Establishments" : "Estabelecimentos";
dictionary['wage'] = lang == 'en' ? "Salary Mass" : "Massa Salarial";
dictionary['gender'] = lang == 'en' ? "Gender" : "Gênero";
dictionary['ethnicity'] = lang == 'en' ? "Ethnicity" : "Etnia";
dictionary['literacy'] = lang == 'en' ? "Literacy" : "Escolaridade";
dictionary['month'] = lang == 'en' ? "Month" : "Mês";
dictionary['port'] = lang == 'en' ? "Port" : "Porto";
dictionary['legal_nature'] = lang == 'en' ? "Legal Nature" : "Natureza Jurídica";
dictionary['size_establishment'] = lang == 'en' ? "Establishment Size " : "Tamanho do Estabelecimento";
dictionary['time_resolution'] = lang == 'en' ? "Time Resolution" : "Resolução Temporal";
dictionary['total_of'] = lang == 'en' ? "Total in selected years: " : "Total nos anos selecionados: ";
dictionary['data_provided_by'] = lang == 'en' ? "Data provided by " : "Dados fornecidos por ";
dictionary['percentage_terms'] = lang == 'en' ? 'Percentage Terms' : 'Termos Percentuais';
dictionary['values'] = lang == 'en' ? 'Values' : 'Valores';
dictionary['exporting_municipality'] = lang == 'en' ? "Based on the Exporting Municipality" : "Baseado nos Municípios Exportadores";
dictionary['state_production'] = lang == 'en' ? "Based on State Production" : "Baseado nos Estados Produtores";
dictionary['establishment_type'] = lang == 'en' ? "Establishment Type" : "Tipo de Estabelecimento";
dictionary['establishments'] = lang == 'en' ? "Establishments" : "Estabelecimentos";
dictionary['sus_bond'] = lang == 'en' ? "SUS Bond" : "Vínculo SUS";
dictionary['bed_type'] = lang == 'en' ? "Bed Type" : "Tipo de Leito";
dictionary['occupation_family'] = lang == 'en' ? "Occupation" : "Ocupação";
dictionary['professionals'] = lang == 'en' ? "Professionals" : "Profissionais";
dictionary['equipment_type'] = lang == 'en' ? "Equipment Type" : "Tipo de Equipamento";
dictionary['equipments'] = lang == 'en' ? "Equipments" : "Equipamentos";

dictionary['equipment_quantity'] = lang == 'en' ? 'Quantity of existing equipment' : 'Quantidade de equipamentos existentes';
dictionary['equipment_quantity_in_use'] = lang == 'en' ? 'Quantity of equipment in use': 'Quantidade de equipamentos em uso';
dictionary['equipment_type'] = lang == 'en' ? 'Equipment Type': 'Tipo de Equipamento';
dictionary['equipment_code'] = lang == 'en' ? 'Equipment Code': 'Código do Equipamento';
dictionary['sus_availability_indicator'] = lang == 'en' ? 'Availability indicator for SUS': 'Indicador de Disponibilidade para o SUS';
dictionary['unit_type'] = lang == 'en' ? 'Unit Type' : 'Tipo de Unidade';

dictionary['number_existing_bed'] = lang == 'en' ? 'Number of Existing Beds' : 'Quantidade de Leitos Existentes';
dictionary['number_sus_bed'] = lang == 'en' ? 'Number of SUS beds' : 'Quantidade de leitos SUS';
dictionary['number_non_sus_bed'] = lang == 'en' ? 'Number of non SUS beds' : 'Quantidade de leitos não SUS';
dictionary['beds'] = lang == 'en' ? 'Beds' : 'Leitos';
dictionary['bed_type'] = lang == 'en' ? 'Type of Bed' : 'Tipo de Leito';
dictionary['bed_type_per_specialty'] = lang == 'en' ? 'Type of Bed / Specialty' : 'Tipo de Leito/Especialidade';
dictionary['health_region'] = lang == 'en' ? 'Health Region' : 'Região de Saúde';

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
            "value": dictionary["data_provided_by"] + dataset.toUpperCase()
        })
        .legend(false)

        if(colorHelper[currentY] != undefined)
            visualization.color(currentY + "_color");

        if(options.indexOf('singlecolor') != -1){
            visualization.color({
                "value" : function(d){
                    return "#4575b4";
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
    y.forEach(function(itemY){
        data = data.map(function(item){
            if(metadatas[itemY][item[itemY]] == undefined){
                // console.log(item[itemY])
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

var loading = dataviva.ui.loading('.loading').text(dictionary.loading);

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
            data = addColor(data);
            data = addOrder(data);
            data = addNameToData(data);
            data = addPercentage(data);
            solo = updateSolo(data);

            loading.hide();
            loadViz(data);
        }
    );
});