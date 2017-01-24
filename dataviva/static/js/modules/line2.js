var lineGraph = document.getElementById('lineGraph'),
    lang = document.documentElement.lang,
    line = lineGraph.getAttribute("line"),
    group = lineGraph.getAttribute("group"),
    dataset = lineGraph.getAttribute("dataset"),
    values = lineGraph.getAttribute("values").split(','),
    value = values[0],
    filters = lineGraph.getAttribute("filters");

// Temporarily translates text until dictionary is updated
dataviva.dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dataviva.dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Município';
dataviva.dictionary['section'] = lang == 'en' ? 'Section' : 'Seção';
dataviva.dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dataviva.dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dataviva.dictionary['by'] = lang == 'en' ? 'by' : 'por';
dataviva.dictionary['of'] = lang == 'en' ? 'of' : 'de';
dataviva.dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';
dataviva.dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dataviva.dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dataviva.dictionary['Y Axis'] = lang == 'en' ? 'Y Axis' : 'Eixo Y';

function string2date(dateString) {
    dateString = dateString.split("-");
    var month = (dateString.length == 2 && dateString[1] !== "0") ? dateString[1] : 1;
    var year = dateString[0];
    return new Date(month+"/01/"+year)
}

var buildData = function(responseApi){

    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = responseApi.headers;

    responseApi.data.forEach(function(item){
        var dataItem = {};

        headers.forEach(function(header){
            dataItem[header] = getAttrByName(item, header);
        });

        if(dataItem[line] != "xx"){
            dataItem["icon"] = "/static/img/icons/" + line + "/" + line + "_" + dataItem[line] + ".png";
            if(dataItem[line] in line_metadata) dataItem[line] = line_metadata[dataItem[line]]['name_' + lang];
            if(dataItem[group] in group_metadata) dataItem[group] = group_metadata[dataItem[group]]['name_' + lang];
            dataItem['date'] = string2date(dataItem['year'] + "-" + dataItem['month'])
            data.push(dataItem);
        }
    });

    return data;
}

var loadViz = function(data){

    var setYAxisLabel = function (type) {
        if (!type) return "Trade Value [$ USD]" //add to dict
        else if (type == 'export') return dataviva.dictionary['exports'] + ' [$ USD]'
        else if (type == 'import') return dataviva.dictionary['imports'] + ' [$ USD]'
    }

    var uiBuilder = {
        'scale': {
            "label": dataviva.dictionary['scale'],
            "type": "drop",
            "value": [{"Linear": "linear"}, {"Log": "log"}],
            "method": function(value, viz){
                viz.y({
                    "scale": value
                }).draw();
            }
        },
        'yaxis': {
            'label': dataviva.dictionary['Y Axis'],
            'value': values,
            'method': function(value, viz){
                viz.y({
                    "value": value,
                    "label": setYAxisLabel(type)
                }).draw();
            }
        },
        'xaxis': {
            'label': dataviva.dictionary['time'],
            'value': [{[dataviva.dictionary['year']]: 'year'}, {[dataviva.dictionary['month']]: 'date'}],
            'method': function(value, viz){
                viz.x({
                    "value": value,
                    "label": dataviva.dictionary['month']
                })
                .time({"value": value})
                .draw();
            }
        }
    };

    var uiComponents = [uiBuilder.scale, uiBuilder.yaxis];
    if (dataset == 'secex') uiComponents.push(uiBuilder.xaxis);

    var titleBuilder = function() {
        var title = 'line: ' + line;
        if (group) {
            title += ', group: ' + group;
        }

        filters.split('&').forEach(function(item) {
            var key = item.split('=')[0],
                value = item.split('=')[1];
            title += ', ' + key + ': ' + value;
        });

        return title;
    };

    var viz = d3plus.viz()
        .container("#lineGraph")
        .data({"value": data, "stroke": {"width": 2}})
        .type("line")
        .id([line, group])
        .background("transparent")
        .shape({"interpolate": "monotone"})
        .x({
            "value": "year",
            "label": {"font": {"size": 20}},
            "ticks": {"font": {"size": 17}
            }
        })
        .y({
            "value": value,
            "label": {"value": setYAxisLabel(type), "font": {"size": 20}},
            "ticks": {"font": {"size": 17}}
        })
        .footer(dataviva.dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title({'total': true, 'value': titleBuilder()})
        .ui(uiComponents)
        .color(line)
        .icon({"value": "icon", "style": "knockout"})
        .time({"value": "year"})
        .axes({"background": {"color": "#FFFFFF"}})
        .draw()
};

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + "...");

$(document).ready(function(){
    url = "http://api.staging.dataviva.info/" + dataset + "/year/" + line + '/' + group + ( filters ? "?" + filters : '');
    if (dataset == 'secex') url = url.replace('/year', '/year/month');

    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + line,
        "http://api.staging.dataviva.info/metadata/" + group
    ],

    function(responses){
        apiData = responses[0];
        line_metadata = responses[1];
        group_metadata = responses[2];

        var data = buildData(apiData);
        data.sort(function(a,b) {return (a['date'] > b['date']) ? 1 : ((b['date'] > a['date']) ? -1 : 0);})

        loading.hide();
        loadViz(data);
    })
});
