var stacked = document.getElementById('stacked'),
    dataset = stacked.getAttribute('dataset'),
    filters = stacked.getAttribute('filters'),
    area = stacked.getAttribute('area'),
    group = stacked.getAttribute('group'),
    depths = stacked.getAttribute('depths').split(' '),
    values = stacked.getAttribute('values').split(' '),
    type = stacked.getAttribute('type').split(' '),
    lang = document.documentElement.lang;

// Temporarily translates text until dictionary is updated
dataviva.dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dataviva.dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Municipio';
dataviva.dictionary['section'] = lang == 'en' ? 'Section' : 'Seção';
dataviva.dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dataviva.dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dataviva.dictionary['by'] = lang == 'en' ? 'by' : 'por';
dataviva.dictionary['of'] = lang == 'en' ? 'of' : 'de';
dataviva.dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dataviva.dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dataviva.dictionary['kg'] = 'KG';
dataviva.dictionary['Based'] =  lang == 'en' ? 'Continent' : 'Baseado';
dataviva.dictionary['year'] =  lang == 'en' ? 'Year' : 'Ano';
dataviva.dictionary['time-resolution'] =  lang == 'en' ? 'Time Resolution' : 'Resolução temporal';
dataviva.dictionary['Order'] =  lang == 'en' ? 'Order' : 'Ordem';
dataviva.dictionary['sort'] =  lang == 'en' ? 'Sort' : 'Ordenar';
dataviva.dictionary['export'] =  lang == 'en' ? 'Export' : 'Exportação';
dataviva.dictionary['import'] =  lang == 'en' ? 'Import' : 'Importação';
dataviva.dictionary['market-share'] =  lang == 'en' ? 'Market Share' : 'Particiação de Mercado';
dataviva.dictionary['y-axis'] = lang == 'en' ? 'Y Axis' : 'Eixo Y';
dataviva.dictionary['desc'] = lang == 'en' ? 'Descending' : 'Descendente';
dataviva.dictionary['asc'] = lang == 'en' ? 'Ascending' : 'Ascendente';
dataviva.dictionary['value'] = lang == 'en' ? 'Value' : 'Valor';
dataviva.dictionary['name'] = lang == 'en' ? 'Name' : 'Nome';
dataviva.dictionary['Year'] = lang == 'en' ? 'Year' : 'Ano';
dataviva.dictionary['Month'] = lang == 'en' ? 'Month' : 'Mês';
dataviva.dictionary['unknown-region'] = lang == 'en' ? 'Unknown Region' : 'Região Desconhecida';

var temp_regionNames = {
    1: "Região Norte",
    2: "Região Nordeste",
    3: "Região Sudeste",
    4: "Região Sul",
    5: "Região Centro-Oeste"
}

var buildData = function(apiData, areaMetadata, groupMetadata) {
    
    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = apiData.headers;

    apiData.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
            });

            dataItem['tooltip_id'] = dataItem[area];

            depths.forEach(function(depth) {
                if (depth != area && depth != group) {
                    if (area == 'product'){
                        // this is due to metadata having only 'chapter' instead of 'product_chapter'
                        depth = depth.split('_')[1]
                        dataItem[depth] = areaMetadata[dataItem[area]][depth]['name_' + lang];
                    } else {
                        dataItem[depth] = areaMetadata[dataItem[area]][depth]['name'];
                    }
                }

                if (area == 'municipality'){
                    if (depth == 'microregion'){
                        dataItem[depth] = dataItem[depth] + ' ';
                    } else if (depth == 'state'){
                        dataItem[depth] = ' ' + dataItem[depth];
                    } else if (depth == 'region'){
                        dataItem[depth] = temp_regionNames[dataItem[depth]];
                    }
                }
            });
            
            dataItem[area] = areaMetadata[dataItem[area]]['name_' + lang];
            
            if (group) {
                if (group == 'product_section' || group == 'continent' || group == 'state'){
                    dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
                }
                if (group != 'region') {
                    // this is due to not having region metadata yet
                    dataItem[group] = groupMetadata[dataItem[group]]['name_' + lang];
                }
            }
            
            if (dataItem.month){
                dataItem.month = dataItem.year + "/" + dataItem.month + "/01";
            }

            data.push(dataItem);
        } catch(e) {

        };
    });

    return data;
}

// Options to set in vizu
var uiHelper = {
    "scale": {
        "label": "Layout",
        "type" : "drop",
        "value" : [
            {
                [dataviva.dictionary['year']]: "linear"
            }, 
            {
                [dataviva.dictionary['market-share']]: "share"
            }
        ],
        "method" : function(value, viz){
            viz.y({
                "scale": value
            })
            .draw();
        }
    },
    // "yaxis": {
    //     "label": dataviva.dictionary['y-axis'],
    //     "type": "drop",
    //     "value": [
    //         {
    //             [dataviva.dictionary['import']]: "import_value"
    //         },
    //         {
    //             [dataviva.dictionary['export']]: "export_value"
    //         }
    //     ],
    //     "method": function(value, viz){
    //         viz.y({
    //             "value": value,
    //             "label": value
    //         }).draw();
    //     }
    // },
    "ysort": {
        "label": dataviva.dictionary['sort'],
        "type": "drop",
        "value": [
            {
                [dataviva.dictionary['desc']] : "desc"
            },
            {
                [dataviva.dictionary['asc']] : "asc"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "sort": value
            }).draw();
        }
    },
    "yorder": {
        "label": dataviva.dictionary['Order'],
        "type": "drop",
        "value": [
            {
                [dataviva.dictionary['value']] : "value"
            },
            {
                [dataviva.dictionary['name']] : "area2"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "value": value
            }).draw();
        }
    },
    "time_range": {
        "label": dataviva.dictionary['time-resolution'],
        "value": [
            {
                [dataviva.dictionary['Year']]: "year"
            },
            {
                [dataviva.dictionary['Month']]: "month"
            }
        ],
        "method": function(value, viz){
            viz.x({
                    "value": value,
                    "label": value
            });
            viz.time({
                "value": value
            }).draw();
        }
    }
};

var loadStacked = function (data, type){
    data_type = {"value": "value", "label": (type == 'export' ? dataviva.dictionary["Total Value Exported"] : dataviva.dictionary["Total Value Imported"]) + ' [$ USD]'};

    var viz = d3plus.viz()
        .title({"value": "Inserir título", "font": {"family": "Times", "size": "24","align": "left"}})
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .y(data_type)  
        .x({"value": "year", "label": ""})
        .time("year")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .title({
            "sub": {"value" : "Inserir sub-título", "font": {"align": "left"}}
        })
        // .legend({"filters": true})
        .footer(dataviva.dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .ui([
            uiHelper.yorder,
            uiHelper.scale,
            uiHelper.ysort,
            // uiHelper.yaxis,
            uiHelper.time_range
        ]);

        if (group) {
            viz.color(group);
        }

        if (depths[0] == '') {
            viz.id({'value': area})
        } else {
            viz.id(depths);
        }

        if (area == "municipality") {
            viz.depth(1)
            viz.order("region")
        }

        viz.draw()
}

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + '...');

$(document).ready(function(){
    var dimensions = [dataset, (dataset == 'secex' ? 'month/year' : 'year') , area];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length)
        dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != area)
            dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + area
    ];

    if (group)
        urls.push('http://api.staging.dataviva.info/metadata/' + group);
    
    ajaxQueue(
        urls,
        function(responses){
            var apiData = responses[0],
                areaMetadata = responses[1];
                groupMetadata = group ? responses[2] : [];

            data = buildData(apiData, areaMetadata, groupMetadata);

            loading.hide();
            loadStacked(data, type);
    });
});