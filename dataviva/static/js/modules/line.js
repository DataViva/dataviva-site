var lineGraph = document.getElementById('lineGraph'),
    dataset = lineGraph.getAttribute('dataset'),
    line = lineGraph.getAttribute('line'),
    yValue = lineGraph.getAttribute('yvalue'),
    baseTitle = lineGraph.getAttribute('graph-title'),
    baseSubtitle = lineGraph.getAttribute('graph-subtitle'),
    args = getUrlArgs(),
    yearRange = args.hasOwnProperty('year') ? [0, +args['year']] : [0, 0],
    depths = args.hasOwnProperty('depths') ? args['depths'].split('+') : DEPTHS[dataset][line] || [line],
    group = depths[0],
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    basicValues = BASIC_VALUES[dataset] || [],
    calcBasicValues = CALC_BASIC_VALUES[dataset] || {},
    currentFilters = {},
    //currentTitleAttrs = {'size': size, 'shapes': squares}
    metadata = {},
    lastYear = 0;

var buildData = function(apiResponse){

    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = apiResponse.headers;

    apiResponse.data.forEach(function(item){
        try{
            var dataItem = {};

            headers.forEach(function(header){
                dataItem[header] = getAttrByName(item, header);
            });

            if (DICT.hasOwnProperty(dataset) && DICT[dataset].hasOwnProperty('item_id') && DICT[dataset]['item_id'].hasOwnProperty(line))
                dataItem[DICT[dataset]['item_id'][line]] = dataItem[line];
            else
                dataItem['id'] = dataItem[line];

            if(group && HAS_ICONS.indexOf(group) >= 0)
                dataItem['icon'] = '/static/img/icons/' + group + '/' + group + '_' + dataItem[group] + '.png';

            depths.forEach(function(depth) {
                if (depth != 'type'){
                    if (depth != line)
                        dataItem[depth] = metadata[line][dataItem[line]][depth]['name_' + lang];
                    else 
                        dataItem[line] = metadata[line][dataItem[line]]['name_' + lang];
                }
            });

            

            //if(type == 'balance') dataItem['icon'] = '/static/img/icons/' + type + '/' + dataItem['type'] + '_val.png';

            //dataItem['date'] = string2date(dataItem['year'] + '-' + dataItem['month'])
            data.push(dataItem);

            //if (dataItem.hasOwnProperty('year') && dataItem['year'] > lastYear)
                //lastYear = dataItem['year'];
        } catch(e) {

        };
    });

    return data;
}

var loadViz = function(data) {

    var viz = d3plus.viz()
        .container('#lineGraph')
        .data({'value': data, 'padding': 0})
        .type('line')
        .shape({'interpolate': 'monotone'})
        .id({
            'value': depths
        })
        .x({
            'value': 'year',
            'label': {'font': {'size': 20}},
            'ticks': {'font': {'size': 17}
            }
        })
        .y({
            'value': 'value',
            //'label': {'value': yAxisLabelBuilder(type), 'font': {'size': 20}},
            'ticks': {'font': {'size': 17}}
        })

        .labels({'align': 'left', 'valign': 'top'})
        .background('transparent')
        .time({'value': 'year'})
    
    viz.draw();

};

var getUrls = function() {
    var dimensions = [dataset, 'year', line],
    metadataAttrs = [];
    
    depths.concat(filters).forEach(function(attr) {
        if (attr != line && dimensions.indexOf(attr) == -1) {
            dimensions.push(attr);
            metadataAttrs.push(attr);
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + lineGraph.getAttribute('filters')]

    //if (dataset == 'secex') urls[0] = urls[0].replace('/year', '/year/month');
    if (line != 'type') urls.push(API_DOMAIN + '/metadata/' + line);

    return urls;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(), 
        function(responses) {
            var data = responses[0];
            metadata[line] = responses[1];

            data = buildData(data);

            // debugger

            loadViz(data);

            loading.hide();
            d3.select('#mask').remove();
        }
    );
});

// Montar o gráfico:
// http://localhost:5000/en/product/021201/trade-partner?menu=exports-destination-line&url=line%2Fsecex%2Fall%2F021201%2Fall%2Fwld%2F%3Fy%3Dexport_val%26color%3Dcolor

// Url:
// http://localhost:5000/en/line/secex/country/value?product=021201
