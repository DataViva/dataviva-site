var tree_map = document.getElementById('tree_map')
    lang = document.documentElement.lang,
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    depths = tree_map.getAttribute('depths') ? tree_map.getAttribute('depths').split(' ') : [],
    group = tree_map.getAttribute('group') || depths[0] || '',
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
dictionary['mesoregion'] = lang == 'en' ? 'Mesoregion' : 'Mesorregião';
dictionary['microregion'] = lang == 'en' ? 'Microregion' : 'Microrregião';
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
                if (group == 'product_section')
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
                viz.id(value == group ? group : [group, value]);
                viz.depth(value == group ? 0 : 1);
                viz.draw();
            },
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
        if (depths.length)
            ui.push(depthSelectorBuilder());
        if (values[0] != '')
            ui.push(sizeSelectorBuilder());
        return ui;
    }

    var titleBuilder = function() {
        return {
            'value': 'Title',
            'font': {
                'size': 22, 
                'align': 'left'
            },
            'sub': {
                'font': {
                    'align': 'left'
                }
            },
            'total': {
                'font': {
                    'align': 'left'
                },
                'value': true
            }
        }
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
        .messages({'branding': true, 'style': 'large' })
        .title(titleBuilder())
        .id(group ? [group, squares] : squares)
        .depth(1)
        .resize(true)
        .ui(uiBuilder());

        if (group) {
            viz.color(group);
        }
        viz.dev(true)
        viz.draw();
};

var loading = dataviva.ui.loading('.loading').text(dictionary['loading'] + '...');

$(document).ready(function() {
    var dimensions = [dataset, 'year', squares];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length)
        dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != squares)
            dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + squares
    ];

    if (group)
        urls.push('http://api.staging.dataviva.info/metadata/' + group);

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