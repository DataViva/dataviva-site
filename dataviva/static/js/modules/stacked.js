var data = [],
    lang = document.documentElement.lang,
    dataset = $("#stacked").attr("dataset"),
    area = $("#stacked").attr("area"),
    filters = $("#stacked").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + area + "/type/" + ( filters ? "?" + filters : '');


var loading = dataviva.ui.loading('.loading');

if (lang == "en")
    loading.text('loading' + "...");
else
    loading.text('carregando' + "...");


var formatData = function(json) {
    json.data.forEach(function(item, index){
        var dataItem = {};

        dataItem["year"] = item[0]
        dataItem["area"] = item[1]

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

// Add continet to contry
var mapCountryToContinent = function(continent_metadata, country_metadata, lang) {

    for (country_index in data){
        for (continent in continent_metadata){
            for (x in continent_metadata[continent].countries){
                if (continent_metadata[continent].countries[x] == data[country_index].area){
                    
                    if (lang == "pt"){
                        data[country_index]["area2"] = continent_metadata[continent].name_pt;                                 
                        data[country_index]["area"] = country_metadata[data[country_index]["area"]].name_pt;                                 
                    }
                    else {
                        data[country_index]["area2"] = continent_metadata[continent].name_en;
                        data[country_index]["area"] = country_metadata[data[country_index]["area"]].name_en;                                 
                    }
                }
            };
        };
    };
}

// Add microrregion and mesorregion to municipality 
var mapMunicipalityToRegions = function(state_metadata, municipality_metadata, lang) {

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
var mapProductToSection = function(product_metadata, lang) {
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

        if (area == "country"){
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

                mapCountryToContinent (continent_metadata, country_metadata, lang);


                areas_depth = ["area2", "area"];

                loading.hide();

                loadStacked(data, areas_depth);
            });
        }

        else if (area == "municipality"){
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

                mapMunicipalityToRegions (state_metadata, municipality_metadata, lang);

                areas_depth = ["area4", "area3", "area2", "area"];

                loading.hide();

                loadStacked(data, areas_depth);
            });
        }

        else if (area == "product"){
            ajaxQueue([
                url,
                "http://api.staging.dataviva.info/metadata/product"
            ],

            function(responses){
                var json = responses[0],
                    product_metadata = responses[1];                

                formatData(json);

                mapProductToSection (product_metadata, lang);

                areas_depth = ["area3", "area2", "area"];

                loading.hide();

                loadStacked(data, areas_depth);
            });
        }
});

