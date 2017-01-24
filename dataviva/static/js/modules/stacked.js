var stacked = document.getElementById('stacked'),
    dataset = stacked.getAttribute("dataset"),
    filters = stacked.getAttribute("filters"),
    area = stacked.getAttribute("area"),
    group = stacked.getAttribute('group'),
    depths = stacked.getAttribute('depths').split(' '),
    values = stacked.getAttribute('values').split(' '),
    lang = document.documentElement.lang

var loading = dataviva.ui.loading('.loading');

// Temporarily translates text until dictionary is updated
dataviva.dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dataviva.dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Municipio';
dataviva.dictionary['section'] = lang == 'en' ? 'Section' : 'Seção';
dataviva.dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dataviva.dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dataviva.dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dataviva.dictionary['by'] = lang == 'en' ? 'by' : 'por';
dataviva.dictionary['of'] = lang == 'en' ? 'of' : 'de';
dataviva.dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';
dataviva.dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dataviva.dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dataviva.dictionary['kg'] = 'KG';


var buildData = function(json) {
    var data = [];

    json.data.forEach(function(item, index){
        var dataItem = {};

        dataItem["year"] = item[0]
        dataItem["month"] = item[0].toString() + "/" + item[1].toString() + "/01"
        dataItem["area"] = item[2]
        dataItem["area2"] = item[3]

        if (item[4] == "export"){
            dataItem["export_value"] = item[5]
            dataItem["export_kg"] = +item[6]
        }
        else {
            dataItem["import_value"] = item[5]
            dataItem["import_kg"] = +item[6]
            }

        data.push(dataItem);
    });

    return data;
}

// Add microrregion and mesorregion to municipality 
var mapMunicipalityToRegions = function(data, state_metadata, municipality_metadata, lang) {

    for (municipality_index in data){
        try {
            data[municipality_index]["area2"] = municipality_metadata[data[municipality_index]["area"]].microrregion.name;
            data[municipality_index]["area3"] = municipality_metadata[data[municipality_index]["area"]].mesorregion.name;

            if (lang == "pt"){
                data[municipality_index]["area4"] = state_metadata[municipality_metadata[data[municipality_index]["area"]].states[0]].name_pt;
                data[municipality_index]["area"] = municipality_metadata[data[municipality_index]["area"]].name_pt;
            } else {
                data[municipality_index]["area4"] = state_metadata[municipality_metadata[data[municipality_index]["area"]].states[0]].name_en;
                data[municipality_index]["area"] = municipality_metadata[data[municipality_index]["area"]].name_en;
            }
        } catch (err) {
            console.log(data[municipality_index]["area"]);
        }
    };
}

// Add the section and chapter of product
var mapProductToSection = function(data, product_metadata, lang) {
    for (product_index in data){
        try {
            data[product_index]["area2"] = product_metadata[data[product_index]["area"]].chapter;
            data[product_index]["area3"] = product_metadata[data[product_index]["area"]].section;

            if (lang == "pt"){
                data[product_index]["area"] = product_metadata[data[product_index]["area"]].name_pt;
            }
            else {
                data[product_index]["area"] = product_metadata[data[product_index]["area"]].name_z;
            }
        } catch (err) {
            console.log(data[product_index]["area"]);
        }
    }
}

// Options to set in vizu
var uiHelper = {
    "scale": {
        "label": "Layout",
        "type" : "drop",
        "value" : [
            {
                "Valor": "linear"
            }, 
            {
                "Participação de Mercado": "share"
            }
        ],
        "method" : function(value, viz){
            viz.y({
                "scale": value
            })
            .draw();
        }
    },

    "yaxis": {
        "label": "Eixo Y",
        "type": "drop",
        "value": [
            {
                "Exportação": "export_value"
            },
            {
                "Importação": "import_value"
            }
        ],
        "method": function(value, viz){
            viz.y({
                "value": value,
                "label": value
            }).draw();
        }
    },
    "ysort": {
        "label": "Ordenar",
        "type": "drop",
        "value": [
            {
                "Ascendente" : "asc"
            },
            {
                "Descendente" : "desc"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "sort": value
            }).draw();
        }
    },
    "yorder": {
        "label": "Ordem",
        "type": "drop",
        "value": [
            {
                "Valor" : "export_value"
            },
            {
                "Nome" : "area2"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "value": value
            }).draw();
        }
    },
    "time_range": {
        "label": "Resolução temporal",
        "value": [
            {
                "Ano": "year"
            },
            {
                "Mês": "month"
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

var loadStacked = function (data, areas_depth){
    var visualization = d3plus.viz()
        .title({"value": "Origens das Importações/Destinos das Exportações dos Soja do Brasil (Jan2000-Mar 2016)", "font": {"family": "Times", "size": "24","align": "left"}})
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .color(areas_depth[0])
        .id(areas_depth)
        .y({"value":"export_value", "label": "Export value"})
        .x({"value": "year", "label": "Year"})
        .time("year")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .legend({
            "order": {
                   "sort": "asc",
                   "value": "id"
                 },
            "filters": true,
        })
        .title({
            "sub": {"value" : "Baseado nos Estados Produtores", "font": {"align": "left"}}
        })
        .ui([
            uiHelper.yorder,
            uiHelper.scale,
            uiHelper.ysort,
            uiHelper.yaxis,
            uiHelper.time_range
        ])
        .draw()
}

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + '...');

$(document).ready(function(){
        var urls = ["http://api.staging.dataviva.info/" + dataset + "/year/month/" + (group ? area + "/" + group : area) + "/type" + ( filters ? "?" + filters : '')    ,
                'http://api.staging.dataviva.info/metadata/' + area
        ];

        if (group)
            urls.push('http://api.staging.dataviva.info/metadata/' + (group == 'section' ? 'product_section' : group));

        if (area == "country"){
            ajaxQueue(
                urls,
                function(responses){

                    var json = responses[0],
                        continent_metadata = responses[1];
                        country_metadata = responses[2];

                    data = buildData (json);

                    debugger;
                    // mapCountryToContinent (data, continent_metadata, country_metadata, lang);


                    areas_depth = ["area2", "area"];

                    loading.hide();
                    loadStacked(data, areas_depth);
            });
        }

        else if (area == "municipality"){
            ajaxQueue([
                urls,
                "http://api.staging.dataviva.info/metadata/state",
            ],

            function(responses){

                var json = responses[0],
                    state_metadata = responses[1];
                    municipality_metadata = responses[2];

                data = buildData(json);

                mapMunicipalityToRegions (data, state_metadata, municipality_metadata, lang);

                areas_depth = ["area4", "area3", "area2", "area"];

                loading.hide();
                loadStacked(data, areas_depth);
            });
        }

        else if (area == "product"){
            ajaxQueue([
                urls
            ],

            function(responses){
                var json = responses[0],
                    product_metadata = responses[1];                

                data = buildData(json);

                mapProductToSection (data, product_metadata, lang);

                areas_depth = ["area3", "area2", "area"];

                loading.hide();
                loadStacked(data, areas_depth);
            });
        }
        else {
            console.log("Unexpected area. Options: product, municipality and country.")
        }
});

