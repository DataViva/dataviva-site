var data = [],
    lang = document.documentElement.lang,
    dataset = $("#radar").attr("dataset"),
    polygon = $("#radar").attr("polygon"),
    label = $("#radar").attr("label"),
    values = $("#radar").attr("values").split(","),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + polygon + "/" + label;

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + polygon,
        "http://api.staging.dataviva.info/metadata/" + label
    ], 

    function(responses){
        var json = responses[0],
            polygon_metadata = responses[1],
            label_metadata = responses[2];

        json.data.forEach(function(item, index){
            var dataItem = {};

            dataItem["year"] = item[0]
            dataItem[polygon] = item[1]
            dataItem[label] = item[2]
            dataItem["average_monthly_wage"] = +item[5]
            dataItem["jobs"] = item[6]

            data.push(dataItem);
        });

        data.map(function(item){
            item["name"] = label_metadata[item[label]]["name_" + lang];
            item[polygon] = polygon_metadata[item[polygon]]["name_" + lang];
        });

        var visualization = d3plus.viz()
            .container("#radar")
            .type("radar")
            .data(data)
            .id([polygon, "name"])
            .color({
                "value": polygon,
                "tooltip": "name"
            })
            .size("jobs")
            .time({
                "value": "year",
                "solo": []
            })
            .background("transparent")
            .draw();
    });
});
