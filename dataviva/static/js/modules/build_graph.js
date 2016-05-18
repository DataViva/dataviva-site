var selectorGraphs = Selector()
    .callback(function(d){
        if ($('#'+selectorGraphs.type()).siblings('input').val() != d.id) {
            $('#'+selectorGraphs.type()).html(d.name);
            $('#dimensions input[name='+selectorGraphs.type()+']').val(d.id).trigger('change');
        }

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
        }

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
        init: init
    }

    var selectedGraph, selectedView, dataset, views;

    function updateViews() {
        $.ajax({
            method: "GET",
            url: "/" + dataviva.language + "/build_graph/views/" + BuildGraph.dataset +"/" +
                $('#dimensions #filter0').val() + "/" +
                ($('#dimensions #filter1').val() == 'all' ? 'all' : $('#dimensions #filter1')[0].name) + "/" +
                ($('#dimensions #filter2').val() == 'all' ? 'all' : $('#dimensions #filter2')[0].name),
            data: {
                    filter1: $('#dimensions #filter1').val(),
                    filter2: $('#dimensions #filter2').val()
                },
            success: function (result) {
                setViews(result.views);

                if ($.inArray(BuildGraph.selectedView, Object.keys(result.views)) > -1) {
                    $('#views select').val(BuildGraph.selectedView);
                } else {
                    BuildGraph.selectedView = result.views[$('#views select').val()].id;
                }

                setGraphs(result.views[BuildGraph.selectedView].graphs);
            }
        });
    }
    function selectGraph(graphLink) {
        BuildGraph.selectedGraph = $(graphLink).attr('id');

        var graphName = $(graphLink).html();

        //Adds active class to selected item
        $(graphLink).parents('.dropdown-menu').find('li').removeClass('active');
        $(graphLink).parent('li').addClass('active');

        //Displays selected text on dropdown-toggle button
        $('#selected-graph').data('graph', $(graphLink).attr('id'));
        $('#selected-graph').html(graphName);

        if (BuildGraph.selectedGraph == 'compare' && !BuildGraph.compare) {
            setCompare();
        } else {
            $('#compare-location').empty();
            delete BuildGraph.compare;
            $('#graph-wrapper').html('<iframe class="embed-responsive-item" src="'+$(graphLink).data('url')+'"></iframe>');
        }
    }

    function setCompare(){
        BuildGraph.compare = $('#compare-location input[name=compare_with]').val();


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

        if ($.inArray(BuildGraph.selectedGraph, Object.keys(graphs)) > -1) {
            selectGraph($('#'+BuildGraph.selectedGraph));
        } else {
            BuildGraph.selectedGraph = $('#selected-graph').data('graph');
            selectGraph($('#selected-graph').siblings('.dropdown-menu').find('li a').first());
        }
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
    }

    function setDimensions(dimensions) {
        $('#dimensions').empty();
        dimensions.forEach(function(dimension, index) {
            var div = $('<div></div>').addClass('form-group'),
                label = $('<label></label>').attr('for', dimension.id).addClass('control-label'),
                cleaner = $('<button></button>').attr('for', dimension.id).addClass('btn btn-xs btn-link pull-right')
                                        .html(dataviva.dictionary['clean_selection'])
                                        .attr('onclick', 'clean_selection('+dimension.id+')'),
                selector = $('<button></button>').attr('id', dimension.id).addClass('btn btn-block btn-outline btn-primary')
                                        .html(dataviva.dictionary['select'])
                                        .attr('onclick', 'select_dimension(id);'),
                filter = $('<input></input>').attr('type', 'hidden').attr('name', dimension.id).attr('id', 'filter'+index).val('all');

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

    function changeDataSet() {
        $('#datasets #dataset-empty-option').remove();
        BuildGraph.dataset = this.value;
        setDimensions(dataviva.datasets[this.value].dimensions);
        updateViews();
    }

    function init() {
        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').change(changeDataSet);
    }
})();


$(document).ready(function () {
    dataviva.requireAttrs(['datasets'], function() {
        BuildGraph.init();
    });
});


