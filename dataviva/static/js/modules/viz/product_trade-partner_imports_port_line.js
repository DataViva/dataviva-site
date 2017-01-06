var data = [];

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/ports"
    ], 

    function(responses){
        responses[1].data.forEach(function(item , index){
            data.push({
                "year": item[0],
                "port": item[1],
                "value": item[2],
                "kg": item[3]
            });
        });

        data.map(function(item){
            item.name = responses[0].ports[item.port];
        });

    var params = {
        title: "Titulo",
        subtitle: "Subtitulo",
        type: "importacao"
    }

    var visualization = d3plus.viz()
        .container("#viz")
        .data(data)
        .type("line")
        .text("name")
        .id("port")
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .x("year")
        .y({
            "value": "value",
            "label": {
                "value": "Valor da " + params.type + " [$ USD]",
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
            }
    })

        .title({
            "font": {"align": "left"},
            "padding": 5,
            "sub": {"font": {"align": "left"}},
            "total": {"font": {"align": "left"}}
        })
        .title(params.title)
        .title({
            "sub": params.subtitle
        })
        .tooltip({
             "value": ["type"]
         })
        .ui([
                {
                    "label": "Escala",
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
                    "label"  : "Eixo Y",
                    "value": [
                        {"Value": "value"},
                        {"KG": "kg"}
                    ],
                    "method": function(value, viz){

                        var label = {
                            "value": "Valor da " + params.type + " [$ USD]",
                            "kg": "Peso total da " + params.type
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
            "value": "year"
        })
        .draw()
    })
});