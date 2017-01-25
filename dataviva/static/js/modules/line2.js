var lineGraph = document.getElementById('lineGraph'),
    lang = document.documentElement.lang,
    line = lineGraph.getAttribute('line'),
    yValue = lineGraph.getAttribute('yvalue'),
    depths = lineGraph.getAttribute('depths') ? lineGraph.getAttribute('depths').split(' ') : [],
    group = lineGraph.getAttribute('group') || depths[0] || '',
    dataset = lineGraph.getAttribute('dataset'),
    values = lineGraph.getAttribute('values').split(' ') || [],
    filters = lineGraph.getAttribute('filters'),
    type = /type=[a-z]*/.exec(filters.split('&'))[0].split('=')[1];

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
dataviva.dictionary['y_axis'] = lang == 'en' ? 'Y Axis' : 'Eixo Y';
dataviva.dictionary['trade_value'] == lang == 'en' ? 'Trade Value' : 'Valor do Comércio';

function string2date(dateString) {
    dateString = dateString.split('-');
    var month = (dateString.length == 2 && dateString[1] !== '0') ? dateString[1] : 1;
    var year = dateString[0];
    return new Date(month + '/01/' + year)
}

var buildData = function(responseApi, lineMetadata, groupMetadata){

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

        if(dataItem[group] != 'xx'){
            dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
            if(dataItem[line] in lineMetadata) dataItem[line] = lineMetadata[dataItem[line]]['name_' + lang];
            if(dataItem[group] in groupMetadata) dataItem[group] = groupMetadata[dataItem[group]]['name_' + lang];
            dataItem['date'] = string2date(dataItem['year'] + '-' + dataItem['month'])
            data.push(dataItem);
        }
    });

    return data;
}

var loadViz = function(data){

    var setYAxisLabel = function (type) {
        if (!type) return dataviva.dictionary['trade_value'] + ' [$ USD]'
        else if (type == 'export') return dataviva.dictionary['exports'] + ' [$ USD]'
        else if (type == 'import') return dataviva.dictionary['imports'] + ' [$ USD]'
    }

    var uiComponents = {
        'scale': {
            'label': dataviva.dictionary['scale'],
            'type': 'drop',
            'value': [{'Linear': 'linear'}, {'Log': 'log'}],
            'method': function(value, viz){
                viz.y({
                    'scale': value
                }).draw();
            }
        },
        'yaxis': {
            'label': dataviva.dictionary['Y Axis'],
            'value': values,
            'method': function(value, viz){
                viz.y({
                    'value': value,
                    'label': setYAxisLabel(type)
                }).draw();
            }
        },
        'xaxis': {
            'label': dataviva.dictionary['time'],
            'value': [{[dataviva.dictionary['year']]: 'year'}, {[dataviva.dictionary['month']]: 'date'}],
            'method': function(value, viz){
                viz.x({
                    'value': value,
                    'label': dataviva.dictionary['month']
                })
                .time({'value': value})
                .draw();
            }
        }
    };

    var uiBuilder = [uiComponents.scale, uiComponents.yaxis];
    if (dataset == 'secex') uiBuilder.push(uiComponents.xaxis);

    var titleBuilder = function() {
         return {
            'value': 'Title',
            'font': {'size': 22, 'align': 'left'},
            'sub': {'font': {'align': 'left'}},
            'total': {'font': {'align': 'left'}},
            'value': true
        }
    };

    var viz = d3plus.viz()
        .container('#lineGraph')
        .data({'value': data, 'stroke': {'width': 2}})
        .type('line')
        .id([group, line])
        .background('transparent')
        .shape({'interpolate': 'monotone'})
        .x({
            'value': 'year',
            'label': {'font': {'size': 20}},
            'ticks': {'font': {'size': 17}
            }
        })
        .y({
            'value': 'value',
            'label': {'value': setYAxisLabel(type), 'font': {'size': 20}},
            'ticks': {'font': {'size': 17}}
        })
        .footer(dataviva.dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleBuilder())
        .ui(uiBuilder)
        .color(group)
        .icon({'value': 'icon', 'style': 'knockout'})
        .time({'value': 'year'})
        .axes({'background': {'color': '#FFFFFF'}})
        .dev(true)
        .draw()
};

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + '...');

$(document).ready(function(){
    var dimensions = [dataset, 'year', line];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length) dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != line) dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters,
        'http://api.staging.dataviva.info/metadata/' + line
    ];

    if (dataset == 'secex') urls[0] = urls[0].replace('/year', '/year/month');

    if (group) urls.push('http://api.staging.dataviva.info/metadata/' + group);

    ajaxQueue(
        urls,
        function(responses){
            var apiData = responses[0],
                lineMetadata = responses[1],
                groupMetadata = group ? responses[2] : [];

            var data = buildData(apiData, lineMetadata, groupMetadata);
            data.sort(function(a,b) {return (a['date'] > b['date']) ? 1 : ((b['date'] > a['date']) ? -1 : 0);})

            loading.hide();
            loadViz(data);
        })
});
