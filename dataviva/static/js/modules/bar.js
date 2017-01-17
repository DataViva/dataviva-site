var data = [],
    solo = [],
    MAX_BARS = 10,
    lang = document.documentElement.lang,
    dataset = $("#bar").attr("dataset"),
    x = $("#bar").attr("x").split(","),
    currentX = x[0],
    y = $("#bar").attr("y").split(","),
    currentY = y[0],
    filters = $("#bar").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + y.join("/") + ( filters ? "?" + filters : '');


// TODO: Title creator
var title = 'Title';
var textHelper = {
    'loading': {
        'en': 'loading ...',
        'pt': 'carregando ...'
    }
};

var visualization;

var loadViz = function(data){
     visualization = d3plus.viz()
        .container("#bar")
        .data(data)
        .type("bar")
        .id({
            'value': currentY,
            'solo': solo
        })
        .y({
            "value": currentY,
            "scale": "discrete" // Manually set Y-axis to be discrete
        })
        .x(currentX)
        .ui([
            {
                'type': 'drop',
                'value': y,
                'method': function(value, viz){
                    viz.y(value)
                       .id({
                            'value': value,
                            'solo': solo
                       })
                       .draw();
                    currentY = value;
                }
            },
            {
                'method': 'x',
                'value': x,
                'type': 'drop'
            }
        ])
        .time('year')
        .draw()
};

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

        data.push(dataItem);
    });

    return data;
}

var addNameToData = function(data){
    y.forEach(function(itemY){
        data = data.map(function(item){
            item[itemY] = metadatas[itemY][item[itemY]]['name_' + lang];

            return item;
        });
    });

    return data;
};

var groupDataByCurrentY = function(data){
    var sumByItem = {};

    data.forEach(function(item){
        if(sumByItem[item[currentY]] == undefined)
            sumByItem[item[currentY]] = {
                "sum": 0,
                "name": item[currentY]
            };

        sumByItem[item[currentY]].sum += item[currentX];
    });

    var list = [];

    for(var item in sumByItem){
        list.push({
            name: sumByItem[item].name,
            sum: sumByItem[item].sum
        });
    }

    return list;
}

var getTopCurrentYNames = function(groupedData){
    var compare = function(a, b){
        if(a.sum < b.sum)
            return 1;
        if(a.sum > b.sum)
            return -1;

        return 0;
    }

    var list = groupedData.sort(compare).slice(0, MAX_BARS);

    var selected = list.map(function(item){
        return item.name;
    });

    return selected;
}

var updateSolo = function(data){
    var copiedData = (JSON.parse(JSON.stringify(data)));
    var groupedData = groupDataByCurrentY(copiedData);
    solo = getTopCurrentYNames(groupedData);

    return solo;
};

var loading = dataviva.ui.loading('.loading').text(textHelper.loading[lang]);

$(document).ready(function(){
    var urls = [url];

    y.forEach(function(item){
        urls.push("http://api.staging.dataviva.info/metadata/" + item);
    });

    ajaxQueue(
        urls, 
        function(responses){
            api = responses.shift();
            metadatas = {};

            y.forEach(function(item, index){
                metadatas[item] = responses[index];
            });

            data = buildData(api);
            data = addNameToData(data);
            solo = updateSolo(data);

            loading.hide();
            loadViz(data);
        }
    );
});