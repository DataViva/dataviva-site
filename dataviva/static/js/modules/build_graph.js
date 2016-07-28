function setDimension(type, name, id) {
    if ($('#'+type).siblings('input').val() != id) {
        $('#'+type).html(name);
        BuildGraph[$('#dimensions input[name='+type+']').attr('id')] = id;
        $('#dimensions input[name='+type+']').val(id).trigger('change');
    }
}

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
            BuildGraph.filterCompare = d.id;
            $('#compare_with').html(d.name);
            $('#compare-location input[name=compare_with]').val(d.id).trigger('change');
        }
        $('#modal-selector').modal('hide');
    });

function select_compare() {
    d3.select("#modal-selector-content").call(selectorCompare.type('bra'));
    $('#modal-selector').modal('show');
}

function clean_selection(button) {
    if ($(button).siblings('input').val() != 'all') {
            BuildGraph[$(button).siblings('input').attr('id')] = 'all';

            if (button.id == 'bra' || button.id == 'compare_with') {
                $(button).html(dataviva.dictionary.brazil);        
            } else {
                $(button).html(dataviva.dictionary['select']);   
            }
        
        $(button).siblings('input').val('all').trigger('change');
    }
}

var BuildGraph = (function () {

    return {
        dataset: dataset,
        views: views,
        selectedView: selectedView,
        selectedGraph: selectedGraph,
        setCompare: setCompare,
        init: init
    }

    var selectedGraph, selectedView, dataset, views, filter0, filter1, filter2, filterCompare;

    function changeDataSet() {
        BuildGraph.filter0 = 'all';
        BuildGraph.filter1 = 'all';
        BuildGraph.filter2 = 'all';
        selectDataSet(this.value);
    }

    function selectDataSet(dataset) {
        $('#datasets #dataset-empty-option').remove();
        BuildGraph.dataset = dataset;
        setDimensions(dataviva.datasets[dataset].dimensions);
        updateViews();
    }

    function setDimensions(dimensions) {
        $('#dimensions').empty();
        dimensions.forEach(function(dimension, index) {
            var div = $('<div></div>').addClass('form-group'),
                filter = $('<input></input>').attr('type', 'hidden').attr('name', dimension.id).attr('id', 'filter'+index).val(BuildGraph['filter'+index]),
                label = $('<label></label>').attr('for', dimension.id).addClass('control-label'),
                button = $('<button></button>').attr('id', dimension.id).addClass('btn btn-block btn-outline btn-primary')
                                        .attr('onclick', 'select_dimension(id);'),
                cleaner = $('<button></button>').attr('for', dimension.id).addClass('btn btn-xs btn-link pull-right')
                                        .html(dataviva.dictionary['clean_selection'])
                                        .attr('onclick', 'clean_selection('+dimension.id+')');

                if (BuildGraph['filter'+index] == 'all') {
                    if(index != 0) {
                        button.html(dataviva.dictionary.select);
                    } else {
                        button.html(dataviva.dictionary.brazil);
                    }

                } else {
                    button.html(dataviva[dimension.id][BuildGraph['filter'+index]].name);
                }
                
            label.html(dataviva.dictionary[dimension.id]);
            filter.change(updateViews);

            if (dimension.name == 'School') {
                div.append(filter);
            } else {
                div.append(filter).append(label).append(button).append(cleaner);
            }

            $('#dimensions').append(div);
        });
    }

    function updateViews() {
        $.ajax({
            method: "GET",
            url: "/" + dataviva.language + "/build_graph/views/" + BuildGraph.dataset +"/" +
                BuildGraph.filter0 + (BuildGraph.filterCompare ? '_' + BuildGraph.filterCompare : '') + "/" +
                (BuildGraph.filter1 == 'all' ? 'all' : $('#dimensions #filter1')[0].name) + "/" +
                (BuildGraph.filter2 == 'all' ? 'all' : $('#dimensions #filter2')[0].name),
            data: {
                    filter1: BuildGraph.filter1,
                    filter2: BuildGraph.filter2
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
            if(BuildGraph.filterCompare) {
                showGraph(graph);
            }
        } else {
            $('#compare-location').empty();
            delete BuildGraph.filterCompare;
            showGraph(graph)
        }

        updateUrl();
    }

    function setCompare(){
        $('#compare-location').empty();

        var div = $('<div></div>').addClass('form-group'),
            label = $('<label></label>').attr('for', 'compare_with').addClass('control-label'),
            cleaner = $('<button></button>').addClass('btn btn-xs btn-link pull-right')
                                    .html(dataviva.dictionary['clean_selection'])
                                    .attr('onclick', 'clean_selection('+'compare_with'+')'),
            button = $('<button></button>').attr('id', 'compare_with').addClass('btn btn-block btn-outline btn-primary')
                                    .attr('onclick', 'select_compare();'),
            filter = $('<input></input>').attr('type', 'hidden').attr('name', 'compare_with').attr('id', 'filterCompare').val(BuildGraph.filterCompare);

        if (BuildGraph.filterCompare) {
            if (BuildGraph.filterCompare == 'all') {
                button.html(dataviva.dictionary.brazil); 
            } else {
                button.html(dataviva.bra[BuildGraph.filterCompare].name);    
            }
        } else {
            button.html(dataviva.dictionary['select'])
        }

        label.html(dataviva.dictionary['compare_with']);
        filter.change(updateViews);

        div.append(filter).append(label).append(button).append(cleaner);

        $('#compare-location').append(div);
    }

    function showGraph(graph) {
        $('#graph-wrapper').html('<iframe class="embed-responsive-item" src="'+$(graph).data('url')+'"></iframe>');
    }

    function init() {
        BuildGraph.dataset = $('#dataset').val();

        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="' + dataset + '"' + 
                (BuildGraph.dataset == dataset ? 'selected' : '') + '>' + 
                                      dataviva.dictionary[dataset] + 
                                     '</option>'));
        }

        $('#datasets').change(changeDataSet);

        BuildGraph.filter0 = $('#filter0').val();
        BuildGraph.filter1 = $('#filter1').val();
        BuildGraph.filter2 = $('#filter2').val();
        BuildGraph.selectedView = $('#view').val();
        BuildGraph.selectedGraph = $('#graph').val();
        BuildGraph.filterCompare = $('#compare').val();

        if(BuildGraph.dataset){
            selectDataSet($('#dataset').val());
        }
    }

    function updateUrl(){
        var url = BuildGraph.dataset +
            '/' + BuildGraph.filter0 + 
            '/' + BuildGraph.filter1 + 
            '/' + BuildGraph.filter2 + 
            '?view=' + BuildGraph.selectedView + 
            '&graph=' + BuildGraph.selectedGraph + 
            (BuildGraph.filterCompare ? '&compare='+BuildGraph.filterCompare : '');

        var newUrl = initialUrl + '/' +url
            window.history.pushState('', '', newUrl);
    }

})();

var initialUrl = window.location.origin + '/' + dataviva.language + '/build_graph'

$(document).ready(function () {
    dataviva.requireAttrs(['datasets', 'bra', 'cnae', 'cbo', 'hs', 'wld', 'course_sc', 'course_hedu', 'university'], function() {
        BuildGraph.init();
    });
});
