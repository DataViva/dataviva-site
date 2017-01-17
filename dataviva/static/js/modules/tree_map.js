var tree_map = document.getElementById('tree_map')
    lang = document.documentElement.lang,
    squares = tree_map.getAttribute('squares'),
    dataset = tree_map.getAttribute('dataset'),
    filters = tree_map.getAttribute('filters'),
    urls = ['http://api.staging.dataviva.info/metadata/' + squares];
    
    if (dataset == 'secex') {
        urls.push('http://api.staging.dataviva.info/' + dataset + '/type/' + squares + '?type=import&' + filters);
        urls.push('http://api.staging.dataviva.info/' + dataset + '/type/' + squares + '?type=export&' + filters);
    } else {
        urls.push('http://api.staging.dataviva.info/' + dataset + '/' + squares + (filters ? '?' + filters : ''));
    }


var buildData = function(responseApi, squaresMetadata){

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

    for (var i = data.length - 1; i >= 0; i--) {
        try {          
            if (squares == 'state')
                data[i][squares] = squaresMetadata[data[i][squares]];
            else
                data[i][squares] = squaresMetadata[data[i][squares]]['name_' + lang];
            if (data[i][squares] === undefined) 
                data.splice(i, 1);
        } catch (e) {
            data.splice(i,1);
        }
    }
    
    return data;
}

var loadViz = function(importData, exportData, flag) {
    var viz = d3plus.viz()
        .container('#tree_map')
        .data(flag == 'import' ? importData : exportData)
        .type('tree_map')
        .id(squares)
        .size('value')
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .ui([
            {
                    'method' : 'size',
                    'value' : ['value', 'kg']
            },
            {
            'method' : function(flag) {
                    viz.data(flag == 'import' ? importData : exportData)
                        .draw();
                },
                'type': 'button',
                'value'  : ['import', 'export']
            }
        ])
        .draw();

};

var loading = dataviva.ui.loading('.loading').text('Loading');

$(document).ready(function(){
    ajaxQueue(
        urls, 
        function(responses){
            var squaresMetadata = responses[0],
                importData = buildData(responses[1], squaresMetadata),
                exportData = buildData(responses[2], squaresMetadata);

            loading.hide();
            loadViz(importData, exportData, 'import');
        })
});