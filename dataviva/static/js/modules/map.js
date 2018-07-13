var map = document.getElementById('map');
var dataset = map.getAttribute('dataset');
var value = map.getAttribute('value');
var apiFilters = map.getAttribute('filters');
var state = map.getAttribute('state');
var area = state ? 'municipality': 'state';
var baseTitle = map.getAttribute('graph-title');
var baseSubtitle = map.getAttribute('graph-subtitle');
var yearRange = [Number.POSITIVE_INFINITY, 0];
var selectedYears = [];
var validOccupations = {};
var currentFilters = {};
var currentTitleAttrs = {'shapes': area};
var metadata = {};
var args = getUrlArgs();
var filters = args.hasOwnProperty('filters') ? args['filters'].split('+') : [];
var values = getUrlArgs().hasOwnProperty('values') ? args['values'].split('+') : [value];
var colors = args.hasOwnProperty('colors') ? args['colors'].split('+') : [];

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
                if (['wage', 'average_wage'].indexOf(header) >= 0) {
                    dataItem[header] = +dataItem[header]
                }
            });

            if (dataItem.hasOwnProperty('occupation_family'))
                validOccupations[dataItem['occupation_family']] = 1;

            dataItem['name'] = metadata[area][dataItem[area]]['name_' + lang];
            dataItem['id_ibge'] = dataItem[area];
            dataItem['id'] = metadata[area][dataItem[area]][area == 'state' ? ('abbr_' + lang) : 'id'];

            for (d in metadata)
                dataItem[d] = metadata[d][dataItem[d]]['name_' + lang];

            if (dataItem.hasOwnProperty('year') && dataItem['year'] > yearRange[1])
                yearRange[1] = dataItem['year'];
            else if (dataItem.hasOwnProperty('year') && dataItem['year'] < yearRange[0])
                yearRange[0] = dataItem['year'];
            if (dataItem.hasOwnProperty('entrants'))
                dataItem.entrants = parseInt(dataItem.entrants)
            if (dataItem.hasOwnProperty('graduates'))
                dataItem.graduates = parseInt(dataItem.graduates)
            if (dataItem.hasOwnProperty('sc_class'))
                dataItem.sc_class = parseInt(dataItem.sc_class)
            data.push(dataItem);
        } catch(e) {

        };
    });

    if (yearRange[0] == yearRange[1])
        yearRange[0] = 0;

    selectedYears = [0, yearRange[1]];

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

        // Adds values selector
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
                   viz.title(titleHelper(yearRange))
                   var d = filteredData();
                    d.forEach(function(item) {
                        if (item[value] == 0)
                            item[value] = null;
                    });

                    viz.data(d)
                        .color(value)
                        .title({'total': {'prefix': dictionary[value] + ': '}})
                        .title(titleHelper(selectedYears))
                        .draw();
                })
             .draw();
        }

        // Adds color selector
        if (colors.length > 1){
            var options = [];
            colors.forEach(function(item) {
                options.push({'id': item, 'label': dictionary[item]});
            });

            d3plus.form()
                .config(config)
                .data(options)
                .title(lang == 'en' ? 'Color' : 'Cor')
                .type(options.length > 3 ? 'drop' : 'toggle')
                .focus(value, function(v) {
                    currentTitleAttrs['value'] = v;
                    selectedColor = v == 'students' ? {'scale':'category20', 'value': args['color'] || v} : {"value": v};
                    viz.color(selectedColor)
                    viz.draw()
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

    var titleHelper = function(years) {
        var header = titleBuilder(baseTitle, baseSubtitle, currentTitleAttrs, dataset, getUrlArgs(), years);

        return {
            'value': header['title'],
            'font': {'size': 22, 'align': 'left'},
            'padding': 5,
            'sub': {'font': {'align': 'left'}, 'value': header['subtitle']},
            'width': window.innerWidth - d3.select('#tools').node().offsetWidth - 20
        };
    };

    var tooltipBuilder = function() {
        return {
            short: {
                '': 'id_ibge',
                [dictionary.basic_values]: [value]
            },
            long: {
                '': 'id_ibge',
                [dictionary.basic_values]: values
            }
        }
    };

    var timelineCallback = function(years) {
        if (!years.length)
            selectedYears = yearRange;
        else if (years.length == 1)
            selectedYears = [0, years[0].getFullYear()];
        else
            selectedYears = [years[0].getFullYear(), years[years.length - 1].getFullYear()]
        toolsBuilder('map', viz, data, titleHelper(selectedYears).value);
        viz.title(titleHelper(selectedYears));
    };

    var viz = d3plus.viz()
        .container('#map')
        .data(data)
        .title(titleHelper(yearRange))
        .title({'total': {'font': {'align': 'left'}}})
        .type('geo_map')
        .coords({'value': '/pt/map/coords/' + state})
        .format(formatHelper())
        .background('transparent')
        .ui(uiBuilder())
        .footer(dictionary['data_provided_by'] + ' ' + dataset.toUpperCase())
        .messages({'branding': true, 'style': 'large'})
        .id('id')
        .time({'value': 'year', 'solo': {'value': yearRange[1], 'callback': timelineCallback}})
        .footer(dictionary['data_provided_by'] + ' ' + (dictionary[dataset] || dataset).toUpperCase())
        .color({'heatmap': ["#282F6B", "#B22200"],
                'value': value})
        .format({
                "text": function(text, params) {
                    var re = new RegExp(state + "[0-9]{5}");
                    if (text.match(re))
                        return metadata[area][text]['name_' + lang];
                    return dictionary[text] || text;
                },
        })
        .height(window.innerHeight - $('#controls').height() - 40)
        .title(titleHelper([0, yearRange[1]]))
        .title({'total': {'font': {'align': 'left'}}})
        .title({'total': {'prefix': dictionary[value] + ': '}});

        if (!state) {
            viz.tooltip({
                '': 'id_ibge', 
                [dictionary.basic_values]: 'name'
            });
        }




        viz.draw();

        if (document.getElementById('controls').style.display = 'none') {
            $('#controls').fadeToggle();
        }

        toolsBuilder('map', viz, data, titleHelper(yearRange).value);
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
    var urls = [
        dimensions[0] == 'sc' ?
        api_url + dimensions.join('/') + '/?' + apiFilters + '&count=sc_class':
            api_url + dimensions.join('/') + '/?' + apiFilters,
        api_url + 'metadata/' + area
    ];

    metadataAttrs.forEach(function(attr) {
        urls.push(api_url + 'metadata/' + attr)
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

            d3.select('#mask').remove();
        }
    );
});
