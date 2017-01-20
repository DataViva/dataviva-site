var data = [],
    lang = document.documentElement.lang,
    dataset = $("#stacked").attr("dataset"),
    label = $("#stacked").attr("label"),
    // country, municipality, product
    division = $("#stacked").attr("division"),
    value = $("#stacked").attr("value"),
    filters = $("#stacked").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + division + "/type/" + ( filters ? "?" + filters : '');


var loading = dataviva.ui.loading('.loading');

if (lang == "en")
    loading.text('loading' + "...");
else
    loading.text('carregando' + "...");


var formatData = function(json) {
    json.data.forEach(function(item, index){
        var dataItem = {};

        dataItem["year"] = item[0]
        dataItem["division"] = item[1]

        if (item[2] == "export"){
            dataItem["export_value"] = item[3]
            dataItem["export_kg"] = +item[4]
        }
        else {
            dataItem["import_value"] = item[3]
            dataItem["import_kg"] = +item[4]
            }

        data.push(dataItem);
    });
}

var mappingCountryToContinent = function(continent_metadata, country_metadata, lang) {

    for (country_index in data){
        for (continent in continent_metadata){
            for (x in continent_metadata[continent].countries){
                if (continent_metadata[continent].countries[x] == data[country_index].division){
                    
                    if (lang == "pt"){
                        data[country_index]["division2"] = continent_metadata[continent].name_pt;                                 
                        data[country_index]["division"] = country_metadata[data[country_index]["division"]].name_pt;                                 
                    }
                    else {
                        data[country_index]["division2"] = continent_metadata[continent].name_en;
                        data[country_index]["division"] = country_metadata[data[country_index]["division"]].name_en;                                 
                    }
                }
            };
        };
    };
}

var mappingMunicipalityToRegions = function(state_metadata, municipality_metadata, lang) {

    for (municipality_index in data){
        try {
        data[municipality_index]["division2"] = municipality_metadata[data[municipality_index]["division"]].microrregion.name;
        data[municipality_index]["division3"] = municipality_metadata[data[municipality_index]["division"]].mesorregion.name;

        if (lang == "pt"){
            data[municipality_index]["division4"] = state_metadata[municipality_metadata[data[municipality_index]["division"]].states[0]].name_pt;
            data[municipality_index]["division"] = municipality_metadata[data[municipality_index]["division"]].name_pt;
        } else {
            data[municipality_index]["division4"] = state_metadata[municipality_metadata[data[municipality_index]["division"]].states[0]].name_en;
            data[municipality_index]["division"] = municipality_metadata[data[municipality_index]["division"]].name_en;
        }
        } catch (err) {
            console.log(data[municipality_index]["division"]);
        }
    };
}

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
            }).draw();
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
                "Nome" : "division2"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "value": value
            }).draw();
        }
    }
};

var loadStacked = function (data, divisions_depth){
    var visualization = d3plus.viz()
        .title({"value": "Origens das Importações/Destinos das Exportações dos Soja do Brasil (Jan2000-Mar 2016)", "font": {"family": "Times", "size": "24","align": "left"}})
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .color(divisions_depth[0])
        .id(divisions_depth)
        .y({"value":"export_value", "label": "Export value"})
        .x({"value": "year", "label": "Year"})
        .time("year")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .legend({
            "filters": true,
        })
        .title({
            "sub": {"value" : "Baseado nos Estados Produtores", "font": {"align": "left"}}
        })
        .ui([
            uiHelper.yorder,
            uiHelper.scale,
            uiHelper.ysort,
            uiHelper.yaxis
        ])
        .draw()
}

$(document).ready(function(){

        if (division == "country"){
            ajaxQueue([
                url,
                "http://api.staging.dataviva.info/metadata/continents",
                "http://api.staging.dataviva.info/metadata/country"
            ],

            function(responses){

                var json = responses[0],
                    continent_metadata = responses[1];
                    country_metadata = responses[2];


                formatData (json);

                mappingCountryToContinent (continent_metadata, country_metadata, lang);


                divisions_depth = ["division2", "division"];

                loading.hide();

                loadStacked(data, divisions_depth);
            });
        }

        else if (division == "municipality"){
            ajaxQueue([
                url,
                "http://api.staging.dataviva.info/metadata/state",
                "http://api.staging.dataviva.info/metadata/municipality"
            ],

            function(responses){

                var json = responses[0],
                    state_metadata = responses[1];
                    municipality_metadata = responses[2];

                formatData(json);

                mappingMunicipalityToRegions (state_metadata, municipality_metadata, lang);

                divisions_depth = ["division4", "division3", "division2", "division"];

                loading.hide();

                loadStacked(data, divisions_depth);
            });
        }

        else if (division == "product"){
            ajaxQueue([
                url,
                "http://api.staging.dataviva.info/metadata/",
                "http://api.staging.dataviva.info/metadata/"
            ],

            function(responses){

                data = mapping (data, lang);

            });
        };
});

