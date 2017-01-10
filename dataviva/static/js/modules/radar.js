var data = [],
    lang = document.documentElement.lang,
    dataset = $("#radar").attr("dataset"),
    polygon = $("#radar").attr("polygon"),
    label = $("#radar").attr("label"),
    value = $("#radar").attr("value"),
    filters = $("#radar").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + polygon + "/" + label + ( filters ? "?" + filters : '');

var pageTitle = window.parent.document.querySelector('h1').childNodes[0].textContent.replace(/\s+/g,' ').trim();
var title;

if(lang == 'en')
    title = 'Economic Activity in ' + pageTitle + ' by gender';
else
    title = 'Atividade Econômica em ' + pageTitle + ' por gênero';

$('#title').html(title);


var loading = dataviva.ui.loading('.loading');
if (lang == "en") {
    loading.text('loading' + "...");
} else {
    loading.text('carregando' + "...");
}

var compare = function(a, b){
    if(a.year < b.year)
        return -1;
    if(a.year > b.year)
        return 1;

    if(a[label] < b[label])
        return -1;
    if(a[label] > b[label])
        return 1;

    return 0;
}


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

        data.sort(compare);
        loading.hide();

        var visualization = d3plus.viz()
            .container("#radar")
            .type("radar")
            .data(data)
            .id([polygon, "name"])
            .color({
                "value": polygon,
                "tooltip": "name"
            })
            .size(value)
            .time({
                "value": "year",
                "solo": []
            })
            .background("transparent")
            .format({
                "number": function(number, params) {
                    var formatted = d3plus.number.format(number, params);
                    if (params.key === "average_monthly_wage") {
                        return "$" + formatted + " USD";
                    }
                    else {
                        return formatted;
                    }
                },
                "text": function(text, params) {
                    if (text === "average_monthly_wage") {
                        return lang == 'en' ? 'Average monthly wage' : 'Salário médio mensal';
                    }
                    else if(text === "jobs") {
                        return lang == 'en' ? 'Jobs' : 'Empregos';
                    }

                    else {
                        return d3plus.string.title(text, params);
                    }

                }
            })
            .draw();
    });
});
