var lineGraph = document.getElementById('lineGraph'),
    lang = document.documentElement.lang,
    line = lineGraph.getAttribute('line'),
    yValue = lineGraph.getAttribute('yvalue'),
    depths = lineGraph.getAttribute('depths') ? lineGraph.getAttribute('depths').split(' ') : [],
    group = lineGraph.getAttribute('group') || depths[0] || '',
    dataset = lineGraph.getAttribute('dataset'),
    values = lineGraph.getAttribute('values').split(' ') || [],
    filters = lineGraph.getAttribute('filters'),
    type = /type=[a-z]*/.test(filters.split('&')) ? /type=[a-z]*/.exec(filters.split('&'))[0].split('=')[1] : 'balance';

// Temporarily translates text until dictionary is updated
dataviva.dictionary['y_axis'] = lang == 'en' ? 'Y Axis' : 'Eixo Y';
dataviva.dictionary['trade_value'] = lang == 'en' ? 'Trade Value' : 'Valor do Comércio';
dataviva.dictionary['trade_balance'] = lang == 'en' ? 'Trade Balance' : 'Balança Comercial';
dataviva.dictionary['exports_imports'] = lang == 'en' ? 'Exports/Imports' : 'Exportações/Importações';
dataviva.dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';

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

        try{
            if(lineMetadata) dataItem[line] = lineMetadata[dataItem[line]]['name_' + lang];

            if(group){
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';
                dataItem[group] = groupMetadata[dataItem[group]]['name_' + lang];
            }

            if(type == 'balance') dataItem['icon'] = '/static/img/icons/' + type + '/' + dataItem['type'] + '_val.png';

            dataItem['date'] = string2date(dataItem['year'] + '-' + dataItem['month'])
            data.push(dataItem);
        }
        catch(e){};
    });

    return data;
}

var buildTradeBalanceData = function(data){

    for (var i = 0; i < data.length; i++) {
        var tradeBalance = {}
        if (i < data.length -1){

            try{
                tradeBalance['date'] = string2date(data[i]['year'] + '-' + data[i]['month'])
                tradeBalance['year'] = data[i]['year']
                tradeBalance['month'] = data[i]['month']
                tradeBalance['balance'] = 'Trade Value';

                if(data[i]['year'] == data[i+1]['year'] && data[i]['month'] != data[i+1]['month']){
                    if(data[i]['type'] == 'export') tradeBalance['value'] = data[i]['value'];
                    else tradeBalance['value'] = -data[i]['value'];
                }

                if(data[i]['year'] == data[i+1]['year'] && data[i]['month'] == data[i+1]['month'] && data[i]['type'] != data[i+1]['type']){
                    if(data[i]['type'] == 'export') tradeBalance['value'] = data[i]['value'] - data[i+1]['value'];
                    else tradeBalance['value'] = data[i+1]['value'] - data[i]['value'];
                    i++;
                }

                tradeBalanceData.push(tradeBalance);

            }catch(e){
                debugger;
            }
        }

    };
};

var loadViz = function(data){

    var yAxisLabelBuilder = function (type) {
        if (type == 'export') return dataviva.dictionary['exports'] + ' [$ USD]'
        if (type == 'import') return dataviva.dictionary['imports'] + ' [$ USD]'
        if (type == 'balance') return dataviva.dictionary['trade_value'] + ' [$ USD]'
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
            'label': dataviva.dictionary['y_axis'],
            'value': values,
            'method': function(value, viz){
                viz.y({
                    'value': value,
                    'label': yAxisLabelBuilder(type)
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
        },
        'balance': {
            'label': dataviva.dictionary['depth'],
            'value': [{[dataviva.dictionary['exports_imports']]: 'type'}, {[dataviva.dictionary['trade_balance']]: 'value'}],
            'method': function(value, viz){
                if(value == 'type') viz.data(data).id(line);
                else viz.data(tradeBalanceData).id('balance');
                viz.draw();
            }
        }
    };

    var uiBuilder = [uiComponents.scale, uiComponents.yaxis];
    if (dataset == 'secex') uiBuilder.push(uiComponents.xaxis);
    if (type == 'balance'){
        uiBuilder.push(uiComponents.balance);
        uiBuilder.splice(uiBuilder.indexOf(uiComponents.yaxis), 1);
    }

    var titleBuilder = function() {
         return {
            'value': 'Title',
            'font': {'size': 22, 'align': 'left'},
            'sub': {'value': 'Subtitle', 'font': {'align': 'left'}},
            'total': {'font': {'align': 'left'}}
        }
    };

    var viz = d3plus.viz()
        .container('#lineGraph')
        .data({'value': data})
        .type('line')
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
            'label': {'value': yAxisLabelBuilder(type), 'font': {'size': 20}},
            'ticks': {'font': {'size': 17}}
        })
        .footer(dataviva.dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .title(titleBuilder())
        .ui(uiBuilder)
        .icon({'value': 'icon', 'style': 'knockout'})
        .legend({'order': {'sort': 'desc','value': 'size'}, "size": 25})
        .time({'value': 'year'})
        .axes({'background': {'color': '#FFFFFF'}})
        .dev(true)

        if (group) viz.id([group, line]).color(group)
        else viz.id(line).color(line)

        viz.draw()
};

var loading = dataviva.ui.loading('.loading').text(dataviva.dictionary['loading'] + '...');

var data = [];
var tradeBalanceData = [];

$(document).ready(function(){
    var dimensions = [dataset, 'year', line];
    if (group && depths.length && depths.indexOf(group) == -1 || !depths.length) dimensions.push(group);
    depths.forEach(function(depth) {
        if (depth != line) dimensions.push(depth);
    });

    var urls = ['http://api.staging.dataviva.info/' + dimensions.join('/') + '?' + filters];

    if (dataset == 'secex') urls[0] = urls[0].replace('/year', '/year/month');

    if (line != 'type') urls.push('http://api.staging.dataviva.info/metadata/' + line);

    if (group) urls.push('http://api.staging.dataviva.info/metadata/' + group);

    ajaxQueue(
        urls,
        function(responses){
            var apiData = responses[0],
                lineMetadata = line != 'type' ? responses[1] : undefined,
                groupMetadata = group ? responses[2] : undefined;

            data = buildData(apiData, lineMetadata, groupMetadata);
            data.sort(function(a,b) {return (a['date'] > b['date']) ? 1 : ((b['date'] > a['date']) ? -1 : 0);})

            if(type == 'balance') buildTradeBalanceData(data);

            loading.hide();
            loadViz(data);
        })
});
