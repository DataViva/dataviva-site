var lang = document.documentElement.lang,
    dataset = $("#line").attr("dataset"),
    line = $("#line").attr("line"),
    group = $("#line").attr("group"),
    filters = $("#line").attr("filters"),
    values = $("#line").attr("values").split(','),
    value = values[0],
    url = "http://api.staging.dataviva.info/" +
        dataset + "/year/" + line + '/' + group + ( filters ? "?" + filters : '');

if (dataset == 'secex') url = url.replace('/year', '/year/month');

var setYAxisLabel = function (type) {
    if (!type) return "Trade Value [$ USD]" //add to dict
    else if (type == 'export') return dataviva.dictionary['exports'] + ' [$ USD]'
    else if (type == 'import') return dataviva.dictionary['imports'] + ' [$ USD]'
}

var uiHelper = {
    'scale': {
        "label": dataviva.dictionary['scale'],
        "type": "drop",
        "value": [
            {
                "Linear": "linear"
            },
            {
                "Log": "log"
            }
        ],

        "method": function(value, viz){
            viz.y({
                "scale": value
            })
            .draw();
        }
    },
    'yaxis': {
        'label': 'Y-Axis', //dataviva.dictionary['Y-Axis'], add to dict
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

var arrayProperties = [uiHelper.scale, uiHelper.yaxis];
if (dataset == 'secex') arrayProperties.push(uiHelper.xaxis);

var formatTooltip = {
    "text": function(text, params) {
        if (dataviva.dictionary[text] != undefined)
            return dataviva.dictionary[text];

        return d3plus.string.title(text, params);
    }
};

var loadViz = function(data){
    var visualization = d3plus.viz()
        .container("#line")
        .data({"value": data, "stroke": {"width": 2}})
        .type("line")
        .id([line, group])
        .background("transparent")
        .shape({
            "interpolate": "monotone"
        })
        .x({
            "value": "year",
             "label": {
                "font": {
                    "size": 20
                }
            },
            "ticks": {
                "font": {
                    "size": 17
                }
            }
        })
        .y({
            "value": value,
            "label": {
                "value": setYAxisLabel(type),
                "font": {
                    "size": 20
                }
            },
            "ticks": {
                "font": {
                    "size": 17
                }
            }
        })
        .ui(arrayProperties)
        .color(line)
        .icon({"value": "icon", "style": "knockout"})
        .time({"value": "year"})
        .axes({"background": {"color": "#FFFFFF"}})
        .draw()
};

function string2date(dateString) {
    dateString = dateString.split("-");
    var month = (dateString.length == 2 && dateString[1] !== "0") ? dateString[1] : 1;
    var year = dateString[0];
    return new Date(month+"/01/"+year)
}

var formatData = function(responseApi){

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

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + "...");

var compare = function(a, b){
    if(a['date'] < b['date'])
        return -1;
    if(a['date'] > b['date'])
        return 1;
    return 0;
}

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + line,
        "http://api.staging.dataviva.info/metadata/" + group
    ],

    function(responses){
        data = responses[0];
        line_metadata = responses[1];
        group_metadata = responses[2];

        var formattedData = formatData(data);
        formattedData.sort(compare)

        loading.hide();
        loadViz(data2);
    })
});
