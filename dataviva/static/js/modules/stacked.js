var data = [],
    lang = document.documentElement.lang,
    dataset = $("#stacked").attr("dataset"),
    label = $("#stacked").attr("label"),

    // country, municipality, product
    division = $(#stacked).attr("division")

    value = $("#stacked").attr("value"),
    filters = $("#stacked").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + division + "/type/" + ( filters ? "?" + filters : '');


var loading = dataviva.ui.loading('.loading');

if (lang == "en")
    loading.text('loading' + "...");
else
    loading.text('carregando' + "...");


var mappingCountryToContinent = function(data, label_metadata) {

    for (country in data){
        for (continent in label_metadata){
            for (x in label_metadata[continent].countries){
                if (label_metadata[continent].countries[x] == data[country].wld_id)
                    data[country]["continent"] = label_metadata[continent].name_pt;                                 
            };
        };
    };

    return data;
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
                "Nome" : "continent"
            }
        ],
        "method": function(value, viz){
            viz.order({
                "value": value
            }).draw();
        }
    }
};

var loadStacked = function (data){
    var visualization = d3plus.viz()
        .title({"value": "Origens das Importações/Destinos das Exportações dos Soja do Brasil (Jan2000-Mar 2016)", "font": {"family": "Times", "size": "24","align": "left"}})
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .color("continent")
        .id("continent")
        .text("continent")
        .y({"value":"export_value", "label": "Export value"})
        .x({"value": "year", "label": "Year"})
        .time("year")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .legend({
            "filters": true,
        })
        .title({
            "sub": {"value" : "Baseado nos Estados Produtores", "font": {"family": "Times", "size": "14","align": "left"}}
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
        ajaxQueue([
            url,
            "http://api.staging.dataviva.info/metadata/continents"
        ],

        function(responses){

            var json = responses[0],
                label_metadata = responses[1];

            json.data.forEach(function(item, index){
                var dataItem = {};

                dataItem["year"] = item[0]
                dataItem["wld_id"] = item[1]

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
            data = mappingCountryToContinent (data, label_metadata);

            loading.hide();

            loadStacked(data);
        });
});

