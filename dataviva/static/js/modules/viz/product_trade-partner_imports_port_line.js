var data = [];
var pageTitle = window.parent.document.querySelector('h1').childNodes[0].textContent.replace(/\s+/g,' ').trim();
var title;

if(lang == 'en')
    title = 'Importation of ' + pageTitle + ' by port';
else
    title = 'Importação de  ' + pageTitle + ' por porto';


var loading = dataviva.ui.loading('.loading');
if (lang == "en") {
    loading.text('loading' + "...");
} else {
    loading.text('carregando' + "...");
}

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/ports"
    ], 

    function(responses){
        responses[0].data.forEach(function(item , index){
            data.push({
                "year": item[0],
                "port": item[1],
                "value": item[2],
                "kg": item[3]
            });
        });

        data.map(function(item){
            item.name = responses[1][item.port];
        });
    
        loading.hide();

        var visualization = d3plus.viz()
            .container("#viz")
            .data(data)
            .type("line")
            .text("name")
            .id("port")
            .background("transparent")
            .shape({"interpolate": "monotone"})
            .x({
                    "value": 'year',
                    'label': {
                        'value': lang == 'en' ? "Year" : "Ano"
                    }
                })
            .y({
                "value": "value",
                "label": {
                        "value": lang == 'en' ? "Value [$ USD]" : "Valor [$ USD]",
                        "font": {
                            "size": 20
                        }
                    }
            })
            .format({
                "number": function(number, params) {
                        
                    var formatted = d3plus.number.format(number, params);
                    if (params.key === "value") {
                        return "$" + formatted + " USD";
                    }
                    else {
                        return formatted;
                    }
                },
                "text": function(text, params) {

                    if (text === "value") {
                        return lang == 'en' ? 'Value' : 'Valor';
                    }
                    else {
                        return d3plus.string.title(text, params);
                    }

                }
            })

            .title({
                "font": {
                    "align": "left",
                    "size": 22,
                    "color": '#888'
                },
                "padding": 5,
                "sub": {"font": {"align": "left"}},
                "total": {"font": {"align": "left"}}
            })
            .title(title)
            .tooltip({
                 "value": ["type"]
             })
            .ui([
                        {
                            "label": lang == 'en' ? "Scale" : "Escala",
                            "type": "drop",
                            "value": [
                                {"Linear": "linear"},
                                {"Log": "log"}
                            ],
                            "method": function(value, viz){
                                viz.y({
                                    "scale": value
                                }).draw();
                            }
                        },
                        {
                            "method" : "y",
                            "label"  : lang == 'en' ? "Y-Axis" : "Eixo Y",
                            "value": lang == 'en' ? [{"Value": "value"}, {"KG": "kg"}] : [{"Valor": "value"}, {"KG": "kg"}],
                            "method": function(value, viz){

                                var label;

                                if(lang == 'en')
                                    label = {
                                        "value": "Value [$ USD]",
                                        "kg": "Amount [KG]"
                                    };
                                else
                                    label = {
                                        "value": "Valor [$ USD]",
                                        "kg": "Quantidade [KG]"
                                    };

                                viz.y({
                                    "value": value,
                                    "label":{
                                        "value": label[value]
                                    }
                                }).draw();
                            }
                        }
                ])
                .time({
                    "value": lang == 'en' ? "Year" : "Ano"
                })
                .draw()
    })
});