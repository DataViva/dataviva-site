function setDimension(type, name, id) {
    if ($('#'+type).siblings('input').val() != id) {
        $('#'+type).html(name);
        $('#dimensions input[name='+type+']').val(id).trigger('change');
    }
}

dataviva.requireAttrs(['datasets', 'bra', 'cnae', 'cbo', 'course_sc', 'course_hedu', 'university'], function() {
    //dataviva.attrs.datasets
    //setDimension(type, name, id)
});

var selectorGraphs = Selector()
    .callback(function(d){
        setDimension(selectorGraphs.type(), d.name, d.id)
        $('#modal-selector').modal('hide');
    });

function select_dimension(id) {
    d3.select("#modal-selector-content").call(selectorGraphs.type(id));
    $('#modal-selector').modal('show');
}

var selectorCompare = Selector()
    .callback(function(d){
        if ($('#compare_with').siblings('input').val() != d.id) {
            $('#compare_with').html(d.name);
            $('#compare-location input[name=compare_with]').val(d.id).trigger('change');
            BuildGraph.compare = d.id;
        }
        BuildGraph.setCompare();
        $('#modal-selector').modal('hide');
    });

function select_compare() {
    d3.select("#modal-selector-content").call(selectorCompare.type('bra'));
    $('#modal-selector').modal('show');
}


function clean_selection(id) {
    if ($(id).siblings('input').val() != 'all') {
        $(id).html(dataviva.dictionary['select']);
        $(id).siblings('input').val('all').trigger('change');
    }
}

var BuildGraph = (function () {

    return {
        dataset: dataset,
        views: views,
        selectedView: selectedView,
        selectedGraph: selectedGraph,
        setCompare: setCompare,
        init: init,
        fillForm: fillForm
    }

    var selectedGraph, selectedView, dataset, views;

    function changeDataSet() {
        $('#datasets #dataset-empty-option').remove();
        BuildGraph.dataset = this.value;
        setDimensions(dataviva.datasets[this.value].dimensions);
        updateViews();
    }

    function setDimensions(dimensions) {
        $('#dimensions').empty();
        dimensions.forEach(function(dimension, index) {
            var div = $('<div></div>').addClass('form-group'),
                filter = $('<input></input>').attr('type', 'hidden').attr('name', dimension.id).attr('id', 'filter'+index).val('all'),
                label = $('<label></label>').attr('for', dimension.id).addClass('control-label'),
                selector = $('<button></button>').attr('id', dimension.id).addClass('btn btn-block btn-outline btn-primary')
                                        .html(dataviva.dictionary['select'])
                                        .attr('onclick', 'select_dimension(id);'),
                cleaner = $('<button></button>').attr('for', dimension.id).addClass('btn btn-xs btn-link pull-right')
                                        .html(dataviva.dictionary['clean_selection'])
                                        .attr('onclick', 'clean_selection('+dimension.id+')');

            label.html(dataviva.dictionary[dimension.id]);
            filter.change(updateViews);

            if (dimension.name == 'School') {
                div.append(filter);
            } else {
                div.append(filter).append(label).append(selector).append(cleaner);
            }

            $('#dimensions').append(div);
        });
    }

    function updateViews() {
        $.ajax({
            method: "GET",
            url: "/" + dataviva.language + "/build_graph/views/" + BuildGraph.dataset +"/" +
                $('#dimensions #filter0').val() +
                ($('#compare-location input[name=compare_with]').val() ? '_' + $('#compare-location input[name=compare_with]').val() : '') + "/" +
                ($('#dimensions #filter1').val() == 'all' ? 'all' : $('#dimensions #filter1')[0].name) + "/" +
                ($('#dimensions #filter2').val() == 'all' ? 'all' : $('#dimensions #filter2')[0].name),
            data: {
                    filter1: $('#dimensions #filter1').val(),
                    filter2: $('#dimensions #filter2').val()
                },
            success: function (result) {
                setViews(result.views);
            }
        });
    }

    function setViews(views) {
        BuildGraph.views = views;
        $('#views').empty()

        var div = $('<div></div>').addClass('form-group');
            select = $('<select></select>').addClass('form-control'),
            label = $('<label></label>').attr('for', 'titles').addClass('control-label'),

        label.html(dataviva.dictionary['views']);

        for(id in views){
            var option = $('<option value="'+id+'">'+views[id].name+'</option>');
            select.append(option);
        }

        select.change(function() {
            BuildGraph.selectedView = this.value;
            setGraphs(BuildGraph.views[this.value].graphs);
        });

        div.append(label).append(select);
        $('#views').append(div);

        // Try to keep the selected view, else keep whatever comes selected
        if ($.inArray(BuildGraph.selectedView, Object.keys(views)) > -1) {
            $('#views select').val(BuildGraph.selectedView);
        } else {
            BuildGraph.selectedView = views[$('#views select').val()].id;
        }

        setGraphs(views[BuildGraph.selectedView].graphs);
    }

    function setGraphs(graphs) {
        $('#graphs').empty()

        var div = $('<div></div>').attr('class', 'dropdown dropdown-select form-group');
            graphButton = $('<button data-toggle="dropdown" aria-expanded="true"></button>')
                            .attr('id', 'selected-graph')
                            .attr('class', 'btn btn-outline btn-block dropdown-toggle'),
            dropDownMenu = $('<ul role="menu" aria-labelledby="selected-graph"></ul>')
                            .attr('class', 'dropdown-menu'),
            label = $('<label></label>').attr('for', 'selected-graph').addClass('control-label');

        label.html(dataviva.dictionary['graphs']);

        for(id in graphs){
            var graphLink = $('<a></a>')
                            .attr('id', id)
                            .attr('class', 'graph-link')
                            .data('url', "/" + dataviva.language + '/embed/' + graphs[id].url)
                            .html('<i class="dv-graph-'+id+' m-r-sm"></i>' + graphs[id].name);

            var graphOption = $('<li role="presentation"></li>').append(graphLink);

            dropDownMenu.append(graphOption);
        }

        div.on( 'click', '.dropdown-menu li a', function(argument) {
           selectGraph(this);
        });

        div.append(label).append(graphButton).append(dropDownMenu);

        $('#graphs').append(div);

        // Try to keep the selected graph, else select the first graph
        if ($.inArray(BuildGraph.selectedGraph, Object.keys(graphs)) > -1) {
            selectGraph($('#'+BuildGraph.selectedGraph));
        } else {
            BuildGraph.selectedGraph = $('#selected-graph').data('graph');
            selectGraph($('#selected-graph').siblings('.dropdown-menu').find('li a').first());
        }
    }

    function selectGraph(graph) {
        BuildGraph.selectedGraph = $(graph).attr('id');

        var graphName = $(graph).html();

        //Adds active class to selected item
        $(graph).parents('.dropdown-menu').find('li').removeClass('active');
        $(graph).parent('li').addClass('active');

        //Displays selected text on dropdown-toggle button
        $('#selected-graph').data('graph', $(graph).attr('id'));
        $('#selected-graph').html(graphName);

        if (BuildGraph.selectedGraph == 'compare') {
            setCompare();
        } else {
            $('#compare-location').empty();
            delete BuildGraph.compare;
            $('#graph-wrapper').html('<iframe class="embed-responsive-item" src="'+$(graph).data('url')+'"></iframe>');
        }
    }

    function setCompare(){
        if (BuildGraph.compare) {
            $('#graph-wrapper').html('<iframe class="embed-responsive-item" src="'+$('#compare').data('url')+'"></iframe>');
        } else {
            $('#compare-location').empty();

            var div = $('<div></div>').addClass('form-group'),
                label = $('<label></label>').attr('for', 'compare_with').addClass('control-label'),
                cleaner = $('<button></button>').attr('for', 'compare_with').addClass('btn btn-xs btn-link pull-right')
                                        .html(dataviva.dictionary['clean_selection'])
                                        .attr('onclick', 'clean_selection('+'compare_with'+')'),
                selector = $('<button></button>').attr('id', 'compare_with').addClass('btn btn-block btn-outline btn-primary')
                                        .html(dataviva.dictionary['select'])
                                        .attr('onclick', 'select_compare();'),
                filter = $('<input></input>').attr('type', 'hidden').attr('name', 'compare_with').attr('id', 'compare_filter').val('all');

            label.html(dataviva.dictionary['compare_with']);
            filter.change(updateViews);

            div.append(filter).append(label).append(selector).append(cleaner);

            $('#compare-location').append(div);
        }
    }

    function init() {
        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').change(changeDataSet);
    }

    function getUrlParameter(sParam) {
        var sPageURL = decodeURIComponent(window.location.search.substring(1)),
            sURLVariables = sPageURL.split('&'),
            sParameterName,
            i;

        for (i = 0; i < sURLVariables.length; i++) {
            sParameterName = sURLVariables[i].split('=');

            if (sParameterName[0] === sParam) {
                return sParameterName[1] === undefined ? true : sParameterName[1];
            }
        }   
    };

    function fillForm(){
        var url = window.location.href.split('?')[0];
        var urlFilters = url.split('build_graph/')[1].split('/');

        //Fill Dataset
        if (urlFilters[0]){
            var dataset = urlFilters[0];
        }

        $('#datasets').val(dataset);
        BuildGraph.dataset = dataset;
        setDimensions(dataviva.datasets[dataset].dimensions);

        //Fill Dimensions
        var filters = {};
        var datasetOption = $('#dimensions div').children('button:even');
        
        filters['f0'] = urlFilters[1];

        if(filters['f0']){
            $('#dimensions #filter0').val(filters['f0']);
            var valueText0 = (filters['f0'] == 'all') ? 'Selected' : dataviva.bra[filters['f0']].name;
            $('#dimensions #bra').text(valueText0);
        }

        var filter1 = datasetOption[1].id;
        var filter2 = (dataset != 'sc') ? datasetOption[2].id : 'course_sc';

        filters['f1'] = urlFilters[2];
        filters['f2'] = urlFilters[3];
        
        if(filters['f1']){
            $('#dimensions #filter1').val(filters['f1']);
            var valueText1 = (filters['f1'] == 'all') ?  'Selected' : dataviva[filter1][filters['f1']].name
            $('#dimensions #'+filter1).text(valueText1);
        }

        if(filters['f2']){
            $('#dimensions #filter2').val(filters['f2']);
            var valueText2 = (filters['f2'] == 'all') ? 'Selected' : dataviva[filter2][filters['f2']].name;
            $('#dimensions #'+filter2).text(valueText2);
        }

        $(document).ajaxComplete(function() {
            
            //Fill Parameters
            if (window.location.href.split('?')[1]){
                var urlParameters = window.location.href.split('?')[1];
                var parameters = {
                    'views': getUrlParameter('views'),
                    'graph': getUrlParameter('graph'),
                    'compare': getUrlParameter('compare'),
                };
            }

            var selectedViews = $('#views');

            $('#views div select option')
                .filter("[value='"+parameters.views+"']")
                .prop('selected', true)
                .siblings()
                .prop('selected', false);
        });

        updateViews();        
    }
})();

$(document).ready(function () {
    dataviva.requireAttrs(['datasets'], function() {
        BuildGraph.init();
        BuildGraph.fillForm();
    });
});


