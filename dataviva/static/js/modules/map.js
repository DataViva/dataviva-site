var map = document.getElementById('map'),
    dataset = map.getAttribute('dataset'),
    value = map.getAttribute('value'),
    apiFilters = map.getAttribute('filters'),
    state = map.getAttribute('state'),
    area = state ? 'municipality': 'state',
    validOccupations = {},
    currentFilters = {},
    metadata = {};

var args = getUrlArgs(),
    filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [],
    values = args.hasOwnProperty('values') ? args['values'].split('+') : SIZES[dataset][area] || [value];

var buildData = function(apiResponse) {

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

            if (dataItem.hasOwnProperty('occupation_family'))
                validOccupations[dataItem['occupation_family']] = 1;

            dataItem['name'] = metadata[area][dataItem[area]]['name_' + lang];
            dataItem['id'] = metadata[area][dataItem[area]][area == 'state' ? ('abbr_' + lang) : 'id'];

            for (d in metadata)
                dataItem[d] = metadata[d][dataItem[d]]['name_' + lang];

            data.push(dataItem);
        } catch(e) {

        };
    });
    return data;
}

var loadViz = function(data){
    var uiBuilder = function() {
        var ui = [];
        config = {
            'id': 'id',
            'text': 'label',
            'font': {'size': 11},
            'container': d3.select('#controls'),
            'search': false
        };

        var filteredData = function() {
            return data.filter(function(item) {
                var valid = true,
                    keys = Object.keys(currentFilters);

                for (var i = 0; i < keys.length; i++) {
                    if (currentFilters[keys[i]] == -1)
                        continue;
                    if (item[keys[i]] != currentFilters[keys[i]]) {
                        valid = false;
                        break;
                    }
                }

                return valid;
            });
        };
        // Adds value selector
        if (values.length > 1) {
           var options = [];
           values.forEach(function(item) {
               options.push({'id': item, 'label': dictionary[item]});
           });

           d3plus.form()
               .config(config)
               .data(options)
               .type('toggle')
               .focus(value, function(value) {
                   viz.title(titleHelper(value))
                   var d = filteredData();
                    d.forEach(function(item) {
                        if (item[value] == 0)
                            item[value] = null;
                    });
                    viz.data(d)
                       .color(value)
                       .draw();
                })
             .draw();
        }

        var statements = function(filter, value){
            if(dictionary['all'] == value)
                return data

            return data.filter(function(item) {
                return  item[filter] == value});
        };

        // Adds filters selector
        filters.forEach(function(filter, j) {
            currentFilters[filter] = -1;
            var options = [];
            for (id in metadata[filter]) {
                if (filter == 'occupation_family' && !validOccupations.hasOwnProperty(id))
                    continue;
                options.push({'id': metadata[filter][id]['name_' + lang], 'label': metadata[filter][id]['name_' + lang]})
            }
            options.sort(function(a, b) {
                if (a['label'] < b['label'])
                    return -1;
                if (a['label'] > b['label'])
                    return 1;
                return 0;
            });

            options.unshift({'id': -1, 'label': dictionary['all']});
            d3plus.form()
                .config(config)
                .data(options)
                .title(dictionary[filter])
                .type('drop')
                .focus(-1, function(value) {
                    currentFilters[filter] = value;
                    viz.data(filteredData());
                    viz.draw();
                })
            .draw();
        });
    };

    var titleHelper = function(value) {
        return {
            'value':  dictionary[value] + ' ' + dictionary['per'] + ' ' + dictionary['state'],
            'font': {'size': 22, 'align': 'left'},
            'total': {'prefix': dictionary[value] + ': '}
        }
    };

    var viz = d3plus.viz()
        .container('#map')
        .data(data)
        .title(titleHelper(value))
        .title({'total': {'font': {'align': 'left'}}})
        .type('geo_map')
        .coords({'value': '/pt/map/coords/' + state})
        .format(formatHelper())
        .tooltip({'sub': 'name'})
        .background('transparent')
        .ui(uiBuilder())
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .id('id')
        .time('year')
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .color({'heatmap': ["#282F6B", "#B22200"],
                'value': value})
        .format({
                "text": function(text, params) {
                    var re = new RegExp(state + "[0-9]{5}")
                    if(text.match(re))
                        return metadata[area][text]['name_' + lang]
                    return text
                },
        })
        .height(window.innerHeight - $('#controls').height() - 40)
        viz.draw();
}


var getUrls = function() {
    var dimensions = [dataset, 'year'];
    var metadataAttrs = [];

    dimensions.push(area);

    filters.forEach(function(attr) {
        if (attr != area && dimensions.indexOf(attr) == -1) {
            dimensions.push(attr);
            metadataAttrs.push(attr);
        }
    });

    var urls = [API_DOMAIN + '/' + dimensions.join('/') + '?' + apiFilters,
        API_DOMAIN + '/metadata/' + area
    ];

    metadataAttrs.forEach(function(attr) {
        urls.push(API_DOMAIN + '/metadata/' + attr)
    });

    return urls;
};

var loading = dataviva.ui.loading('.loading').text(dictionary['Building Visualization']);

$(document).ready(function() {
    ajaxQueue(
        getUrls(),
        function(responses) {
            var data = responses[0];
            metadata[area] = responses[1];

            filters.forEach(function(filter, i) {
                metadata[filter] = responses[2+i];
            });

            data = buildData(data);
            loadViz(data);


            // loading.hide();
            d3.select('#mask').remove();
        }
    );
});
