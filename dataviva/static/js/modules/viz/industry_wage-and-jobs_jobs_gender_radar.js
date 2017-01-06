var data = [];

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/cnae_sections"
    ], 

    function(responses){
        responses[1].data.forEach(function(item , index){
            data.push({
                "year": item[0],
                "gender": item[1] == "1" ? "Male" : "Female",
                "cnae_section": item[2],
                "average_monthly_wage": +item[5],
                "jobs": item[6]
            });
        });

        data.map(function(item){
            item.name = responses[0].cnae_sections[item.cnae_section].name_pt;
        });

        var visualization = d3plus.viz()
            .container("#viz")
            .type("radar")
            .data(data)
            .id(["gender", "name"])
            .color({
                "value": "gender",
                "tooltip": "name"
            })
            .size("average_monthly_wage")
            .time({
                "value": "year",
                "solo": []
            })
            .format({
                "text": function(text, params) {
                    if (text === "average_monthly_wage") {
                        return "Salário Médio Mensal";
                    }
                    else {
                        return d3plus.string.title(text, params);
                    } 
                },

                "number": function(number, params) {
                    
                var formatted = d3plus.number.format(number, params);
                if (params.key === "average_monthly_wage") {
                    return "$" + formatted + " USD";
                }
                else {
                    return formatted;
                }
            }
            
            })
            .background("transparent")
            .draw();

    });
});


