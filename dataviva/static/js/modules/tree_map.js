var tree_map = document.getElementById('tree_map')
    lang = document.documentElement.lang,
    squares = tree_map.getAttribute('squares'),
    group = tree_map.getAttribute('group'),
    dataset = tree_map.getAttribute('dataset'),
    filters = tree_map.getAttribute('filters'),
    urls = ['http://api.staging.dataviva.info/metadata/' + squares,
            'http://api.staging.dataviva.info/metadata/' + (group == 'section' ? 'product_section' : group),
            'http://api.staging.dataviva.info/' + dataset + '/year/' + squares + '/' + group + '?' + filters
    ];

var buildData = function(responseApi, squaresMetadata, groupMetadata){

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
            data[i][squares] = squaresMetadata[data[i][squares]]['name_' + lang];
            data[i][group] = groupMetadata[data[i][group]]['name_' + lang];
        } catch (e) {
            data.splice(i, 1);
        }
    }

    return data;
}

var loadViz = function(data) {
    var viz = d3plus.viz()
        .container('#tree_map')
        .data(data)
        .type('tree_map')
        .id([group, squares])
        .depth(1)
        .color(group)
        .size('value')
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .legend({"size": 50})
        .ui([
            {
                'method' : 'size',
                'label': '',
                'value' : [{[dictionary['value']]: 'value'}, 'kg']
            },
        ])
        .format({
            'text': function(text) {
                return text == 'value' || text == 'share' ? dictionary[text] : text;
            }
        })
        .time('year')
        .draw();
};

var loading = dataviva.ui.loading('.loading').text(dictionary['loading']);

$(document).ready(function(){
    ajaxQueue(
        urls, 
        function(responses){
            var squaresMetadata = responses[0],
                groupMetadata = responses[1],
                data = buildData(responses[2], squaresMetadata, groupMetadata);

            loading.hide();
            loadViz(data);
        })
});