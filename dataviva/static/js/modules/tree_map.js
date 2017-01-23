var tree_map = document.getElementById('tree_map')
    lang = document.documentElement.lang,
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    group = tree_map.getAttribute('group'),
    depths = tree_map.getAttribute('depths').split(' '),
    values = tree_map.getAttribute('values').split(' '),
    dataset = tree_map.getAttribute('dataset'),
    filters = tree_map.getAttribute('filters');

// Temporarily translates text until dictionary is updated
dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Municipio';
dictionary['section'] = lang == 'en' ? 'Section' : 'Seção';
dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dictionary['by'] = lang == 'en' ? 'by' : 'por';
dictionary['of'] = lang == 'en' ? 'of' : 'de';
dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';
dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dictionary['kg'] = 'KG';


var buildData = function(apiResponse, squaresMetadata, groupMetadata) {

    var getAttrByName = function(item, attr) {
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item) {
        try {
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
            });

            dataItem[squares] = squaresMetadata[dataItem[squares]]['name_' + lang];
            if (group) {
                if (group == 'section')
                    dataItem['icon'] = '/static/img/icons/' + group + '/section_' + dataItem[group] + '.png';
                dataItem[group] = groupMetadata[dataItem[group]]['name_' + lang];
            }

            data.push(dataItem);
        } catch(e) {

        };
    });

    return data;
}

var loadViz = function(data) {

    var depthSelectorBuilder = function() {
        var array = depths.slice(0);
        array.splice(array.indexOf(squares), 1);
        array.splice(0, 0, squares);
        array.forEach(function(item, i){
            array[i] = {[dictionary[item]] : item};
        });

        return {
            'method': function(value) {
                viz.depth(depths.indexOf(value));
                viz.draw();
            },
            'default': depths.indexOf(squares),
            'type': 'drop',
            'label': dictionary['depth'],
            'value': array
        };
    };

    var sizeSelectorBuilder = function() {
        var options = [];
        values.forEach(function(item) {
            options.push({[dictionary[item]]: item});
        });
        return {
            'method' : 'size',
            'label': dictionary['value'],
            'value' : options
        };
    };

    var uiBuilder = function() {
        ui = [];
        if (depths[0] != '')
            ui.push(depthSelectorBuilder());
        if (values[0] != '')
            ui.push(sizeSelectorBuilder());
        return ui;
    }

    var titleBuilder = function() {
        var title = 'squares: ' + squares;
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
        .container('#tree_map')
        .data(data)
        .type('tree_map')
        .size(size)
        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time('year')
        .format('pt_BR')
        .icon({'value': 'icon', 'style': 'knockout'})
        .legend({'filters': true, 'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({
            'branding': true,
            'style': 'large'
        })
        .title({'total': true, 'value': titleBuilder()})
        .ui(uiBuilder());

        if (group) {
            viz.color(group);
        }

        if (depths[0] == '') {
            viz.id({'value': squares})
        } else {
            viz.id({'value': depths});
            viz.depth(depths.indexOf(squares));
        }

        viz.draw();
};

var loading = dataviva.ui.loading('.loading').text(dictionary['loading'] + '...');

$(document).ready(function() {
    var urls = ['http://api.staging.dataviva.info/' + dataset + '/year/' + squares + '/' + group + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + squares
    ];

    if (group)
        urls.push('http://api.staging.dataviva.info/metadata/' + (group == 'section' ? 'product_section' : group));

    ajaxQueue(
        urls, 
        function(responses){
            var data = responses[0],
                squaresMetadata = responses[1],
                groupMetadata = group ? responses[2] : [];

            data = buildData(data, squaresMetadata, groupMetadata);

            loading.hide();
            loadViz(data);
        })
});