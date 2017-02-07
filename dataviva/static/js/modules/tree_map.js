var tree_map = document.getElementById('tree_map')
    lang = document.documentElement.lang,
    dataset = tree_map.getAttribute('dataset'),
    squares = tree_map.getAttribute('squares'),
    size = tree_map.getAttribute('size'),
    filters = tree_map.getAttribute('filters');
    depths = tree_map.getAttribute('depths') ? tree_map.getAttribute('depths').split(' ') : [],
    sizes = tree_map.getAttribute('sizes') ? tree_map.getAttribute('sizes').split(' ') : [],
    group = tree_map.getAttribute('group') || depths[0] || '',
    controls = true;

// Temporarily translates text until dictionary is updated
dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Municipio';
dictionary['product_section'] = lang == 'en' ? 'Section' : 'Seção';
dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dictionary['by'] = lang == 'en' ? 'by' : 'por';
dictionary['of'] = lang == 'en' ? 'of' : 'de';
dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';
dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dictionary['mesoregion'] = lang == 'en' ? 'Mesoregion' : 'Mesorregião';
dictionary['microregion'] = lang == 'en' ? 'Microregion' : 'Microrregião';
dictionary['region'] = lang == 'en' ? 'Region' : 'Região';
dictionary['basic_values'] = lang == 'en' ? 'Basic Values' : 'Valores Básicos';
dictionary['ibge_id'] = lang == 'en' ? 'IBGE ID' : 'ID IBGE';
dictionary['cnae_id'] = lang == 'en' ? 'CNAE ID' : 'ID CNAE';
dictionary['wld_id'] = lang == 'en' ? 'WLD ID' : 'ID WLD';
dictionary['hs_id'] = lang == 'en' ? 'HS ID' : 'ID HS';
dictionary['market_share'] = lang == 'en' ? 'Market Share' : 'Participação de Mercado';
dictionary['item_id'] = 'ID';
dictionary['per'] = lang == 'en' ? 'per' : 'por';
dictionary['exports_weight'] = lang == 'en' ? 'Export Weight' : 'Peso das Exportações';
dictionary['imports_weight'] = lang == 'en' ? 'Import Weight' : 'Peso das Importações';
dictionary['imports_per_weight'] = lang == 'en' ? 'Imports per kg' : 'Importações por peso';
dictionary['exports_per_weight'] = lang == 'en' ? 'Exports per kg' : 'Exportações por peso';
dictionary['kg'] = 'KG';

var formatDict = {
    'secex': {
        'share': 'market_share',
        'item_id': {
            'municipality': 'ibge_id',
            'product': 'hs_id',
            'country': 'wld_id'
        },
        'kg': {
            'export': 'exports_weight',
            'import': 'exports_weight'
        },
        'value': {
            'export': 'exports',
            'import': 'imports'
        },
        'value_per_kg': {
            'export': 'exports_per_weight',
            'import': 'imports_per_weight'
        }
    }
};

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

            dataItem[formatDict[dataset]['item_id'][squares]] = dataItem[squares];

            depths.forEach(function(depth) {
                if (depth != squares && depth != group) {
                    dataItem[depth] = squaresMetadata[dataItem[squares]][depth]['name'];
                }
            });
            
            dataItem[squares] = squaresMetadata[dataItem[squares]]['name_' + lang];
            
            if (group) {
                if (group == 'product_section' || group == 'continent')
                    dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
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
        sizes.forEach(function(item) {
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
        if (sizes.length)
            ui.push(sizeSelectorBuilder());
        return ui;
    }

    var titleBuilder = function() {
        return {
            'value': 'Title',
            'font': {'size': 22, 'align': 'left'},
            'sub': {'font': {'align': 'left'}, 'value': 'Subtitle'},
            'total': {'font': {'align': 'left'}, 'value': true}
        }
    };

    var tooltipBuilder = function() {
        return {
            'short': {
                '': ['item_id'],
                [dictionary['basic_values']]: [size]
            },
            'long': {
                '': ['item_id'],
                [dictionary['basic_values']]: sizes.length ? sizes : [size]
            }
        }
    };

    var getUrlArgs = function() {
        var args = {};
        window.location.search.split('?')[1].split('&').forEach(function(arg) {
            args[arg.split('=')[0]] = arg.split('=')[1];
        })
        return args;
    };

    var formatHelper = function() {
        var args = getUrlArgs();

        return {
            'text': function(text, key) { 
                switch (text) {
                    case 'item_id':
                        return dictionary[formatDict[dataset][text][squares]] || dictionary[text];
                    case 'value':
                    case 'kg':
                    case 'value_per_kg':
                        return dictionary[formatDict[dataset][text][args['type']]];
                    default:
                        return dictionary[text] || text;
                };
                
            },
            'number': function(value, opts) {
                var result;

                if (value.toString().split('.')[0].length > 3) {

                    var symbol = d3.formatPrefix(value).symbol;
                    symbol = symbol.replace('G', 'B');
                    
                    value = d3.formatPrefix(value).scale(value);
                    value = parseFloat(d3.format('.3g')(value));

                    if (symbol && lang === 'pt') {
                        var digit = parseFloat(value.toString().split('.')[0]);
                        switch (symbol) {
                            case 'T':
                                symbol = digit < 2 ? ' Trilh\u00e3o' : ' Trilh\u00f5es';
                                break;
                            case 'B':
                                symbol = digit < 2 ? ' Bilh\u00e3o' : ' Bilh\u00f5es';
                                break;
                            case 'M':
                                symbol = digit < 2 ? ' Milh\u00e3o' : ' Milh\u00f5es';
                                break;
                            case 'k':
                                symbol = ' Mil';
                        }
                    }

                    result = value + symbol;
                }
                
                switch (opts.key) {
                    case 'share':
                        result = d3.round(value, 2) + '%';
                        break;
                    case 'value':
                        result = '$' + result + ' USD';
                        break;
                    case 'kg':
                        result += ' kg';
                };

                if (lang == 'pt') {
                    var n = result.split('.')
                    n[0] = n[0].replace(',', '.')
                    result = n.join(',')
                }

                return result;
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
        .icon(group == 'state' ? {'value': 'icon'} : {'value': 'icon', 'style': 'knockout'})
        .legend({'filters': true, 'order': {'sort': 'desc', 'value': 'size'}})
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large' })
        .title(titleBuilder())
        .id(group ? [group, squares] : squares)
        .depth(1)
        .tooltip(tooltipBuilder())
        .format(formatHelper())
        .ui(uiBuilder());

    if (group)
        viz.color({'scale':'category20', 'value': group});

    viz.draw();

    toolsBuilder(viz, data, titleBuilder().value, uiBuilder());
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
        function(responses) {
            var data = responses[0],
                squaresMetadata = responses[1],
                groupMetadata = group ? responses[2] : [];

            data = buildData(data, squaresMetadata, groupMetadata);

            loading.hide();
            loadViz(data);
        }
    );
});
