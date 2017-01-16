var data = [],
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


var loadViz = function(data){
     var visualization = d3plus.viz()
        .container("#bar")
        .data(data)
        .type("bar")
        .id(y[0])
        .y(y[0])
        .y({"scale": "discrete"}) // Manually set Y-axis to be discrete
        .x(x[0])
        .ui([
            {
                'value': y,
                'type': 'drop',
                'method': function(value, viz){
                    var filteredData = processData(data);
                    console.log(filteredData);
                    viz.data(filteredData).y(value).id(value).draw();
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

var processData = function(data){
    

    var filterDataBySelectedYears = function(data){
        var getSelectedYears = function(data){
            var years = new Set();

            data.forEach(function(item){
                years.add(item.year);
            });

            return Array.from(years);
        };

        var years = getSelectedYears(data);

        data = data.filter(function(item){
            return years.indexOf(item.year) != -1;
        });

        return data;
    };

    var filterTopData = function(data){
        var getTopCurrentYNames = function(groupedData){
            var compare = function(a, b){
                if(a.sum < b.sum)
                    return 1;
                if(a.sum > b.sum)
                    return -1;

                return 0;
            }

            var list = groupedData.sort(compare).slice(0, 10);

            var selected = list.map(function(item){
                return item.name;
            });

            return selected;
        }

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

        var groupedData = groupDataByCurrentY(data);
        var topCurrenYNames = getTopCurrentYNames(groupedData);

        data = data.filter(function(item){
            return topCurrenYNames.indexOf(item[currentY]) != -1;
        })

        return data;
    }

    var filteredData = (JSON.parse(JSON.stringify(data)));

    filteredData = filterDataBySelectedYears(filteredData);
    filteredData = filterTopData(filteredData);

    return filteredData;
}

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
            filteredData = processData(data);

            loading.hide();
            loadViz(filteredData);
        }
    );
});