var map = document.getElementById('map'),
    dataset = map.getAttribute('dataset'),
    value = map.getAttribute('value'),
    lang = 'pt';
    filters = map.getAttribute('filters');

var buildData = function(apiResponse,metadata) {

    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    };

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header) {
                dataItem[header] = getAttrByName(item, header);
            });
            dataItem['id'] = metadata[dataItem['state']]['abbr_' + lang];
            data.push(dataItem);
        } catch(e) {

        };
    });

    return data;
}



var loadViz = function(data){
    var visualization = d3plus.viz()
        .container('#viz')
        .data(data)
        .type('geo_map')
        .coords({'value': '/pt/map/coords'})
        .format(formatHelper())
        .id('id')
        .time('year')
        .color({'heatmap': ["#282F6B", "#B22200"],
                'value': value})
        .draw()
}


$(document).ready(function() {
    ajaxQueue(
        ['http://api.staging.dataviva.info/'+dataset +'/year/state?'+filters, 'http://api.staging.dataviva.info/metadata/state'], 
        function(responses) {
            var data = responses[0];

            var metadata = responses[1]

            data = buildData(data,metadata);

            loadViz(data);


            // loading.hide();
            d3.select('#mask').remove();
        }
    );
});
