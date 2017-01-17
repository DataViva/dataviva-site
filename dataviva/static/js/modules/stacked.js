var data = []
var title;
var type = ""
var lang = "en"

// if(type == 'import'){
//     if(lang == 'en')
//         title = 'Importation of ' + pageTitle + ' by port';
//     else
//         title = 'Importação de  ' + pageTitle + ' por porto';
// }
// else {
//     if(lang == 'en')
//         title = 'Exportation of ' + pageTitle + ' by port';
//     else
//         title = 'Exportação de  ' + pageTitle + ' por porto';   
// }

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
        "label": "Escala",
        "type" : "drop",
        "value" : [
            {
                "Valor": "linear"
            }, 
            {
                "Porcentagem": "share"
            }
        ],
        "method" : function(value, viz){
            viz.y({
                "scale": value
            }).draw();
        }
    },

    "yaxis": {
        "label": "Import/Export",
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
        .title("Origens das Importações/Destinos das Exportações dos Soja do Brasil (Jan2000-Mar 2016)")
        .axes({"background": {"color": "white"}})
        .container("#stacked")
        .type("stacked")
        .data(data)
        .color("continent")
        .id("continent")
        .text("continent")
        .y({"value":"export_value", "label": "Export value"})
        .order({"value":"export_value", "sort":"asc"})
        .x({"value": "year", "label": "Year"})
        .time("year")
        .background("transparent")
        .messages({"style": "large", "branding": true})
        .shape({"interpolate": "monotone"})
        .legend({
            "data": true,
            "size": [25,25],
            "filters": true,
            "sort": "asc",
            "value": "size"
        })
        .title({
            "sub": {"value" : "Baseado nos Estados Produtores", "font": {"family": "Times", "color": "#756bb1", "size": "14","align": "left"}},
            "total": true,
            "font": {"align": "left"},
            "padding": 5,
            "align": "left"
        })
        .ui([
            uiHelper.scale,
            uiHelper.yaxis,
            uiHelper.ysort,
            uiHelper.yorder
        ])
        .draw()
}

$(document).ready(function(){
        ajaxQueue([
            "http://api.staging.dataviva.info/secex/year/country/type/?product=1201",
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

