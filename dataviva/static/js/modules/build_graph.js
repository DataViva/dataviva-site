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

function clean_selection(id) {
    if ($(id).siblings('input').val() != 'all') {
        $(id).html(dataviva.dictionary['select']);
        $(id).siblings('input').val('all').trigger('change');
    }
}

var BuildGraph = (function () {

    return {
        dataset: dataset,
        selectedView: selectedView,
        views: views,
        init: init
    }

    var selectedView, dataset;

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
            }
        });
    }

    function selectView() {
        BuildGraph.selectedView = this.value;
        setGraphs(BuildGraph.views[this.value].graphs);
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

        select.change(selectView);

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
                div.append(filter).append(label).append(cleaner).append(selector);
            }

            $('#dimensions').append(div);
        });
    }

    function setGraphs(graphs) {
        $('#graphs').empty()

        var div = $('<div></div>').attr('class', 'dropdown dropdown-select form-group');
            graphButton = $('<button data-toggle="dropdown" aria-expanded="true"></button>')
                            .attr('id', 'graph-button')
                            .attr('class', 'btn btn-outline btn-block dropdown-toggle'),
            dropDownMenu = $('<ul role="menu" aria-labelledby="graph-button"></ul>')
                            .attr('class', 'dropdown-menu'),
            label = $('<label></label>').attr('for', 'graph-button').addClass('control-label');

        label.html(dataviva.dictionary['graphs']);

        for(id in graphs){
            var graphLink = $('<a></a>')
                            .attr('href', "/" + dataviva.language + '/embed/' + graphs[id].url)
                            .attr('target', "graphs-frame-build-graphs")
                            .html('<i class="dv-graph-'+id+' m-r-sm"></i>' + graphs[id].name);

            var graphOption = $('<li role="presentation"></li>').append(graphLink);

            dropDownMenu.append(graphOption);
        }

        div.on( 'click', '.dropdown-menu li a', function() {
           var target = $(this).html();

           //Adds active class to selected item
           $(this).parents('.dropdown-menu').find('li').removeClass('active');
           $(this).parent('li').addClass('active');

           //Displays selected text on dropdown-toggle button
           $(this).parents('.dropdown-select').find('.dropdown-toggle').html(target);
        });

        div.append(label).append(graphButton).append(dropDownMenu);
        $('#graphs').append(div);
    }

    function changeDataSet() {
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


