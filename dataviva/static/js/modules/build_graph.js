var selectorGraphs = Selector()
    .callback(function(d){
        $('#'+selectorGraphs.type()).html(d.name);
        $('#dimensions input[name='+selectorGraphs.type()+']').val(d.id).trigger('change');
        $('#modal-selector').modal('hide');
    });

function select_dimension(id) {
  d3.select("#modal-selector-content").call(selectorGraphs.type(id));
  $('#modal-selector').modal('show');
}

function clean_selection(id) {
  $(id).siblings('button').html('Select');
  $(id).siblings('input').val('all').trigger('change');
}

var buildGraph = (function () {

    return {
        dataset: dataset,
        views: views,
        init: init
    }

    var views, dataset;

    function setDimensions(dimensions) {
        $('#dimensions').empty();
        dimensions.forEach(function(dimension, index) {
            var div = $('<div></div>').addClass('form-group'),
            label = $('<label></label>').attr('for', dimension.id).addClass('control-label'),
            deactivate_button = $('<button></button>').attr('for', dimension.id).addClass('btn btn-xs btn-link pull-right')
                                    .html(dataviva.dictionary['deactivate'])
                                    .attr('onclick', 'clean_selection(this)'),
            selector_button = $('<button></button>').attr('id', dimension.id).addClass('btn btn-block btn-outline btn-primary')
                                    .html(dataviva.dictionary['select'])
                                    .attr('onclick', 'select_dimension(id);');

            filter = $('<input></input>').attr('type', 'hidden').attr('name', dimension.id).attr('id', 'filter'+index).val('all');

            label.html(dataviva.dictionary[dimension.id]);

            if (dimension.name == 'School') {
                div.append(filter);
            } else {
                div.append(filter).append(label).append(deactivate_button).append(selector_button);
            }

            $('#dimensions').append(div);
        });
    }

    function setViews(views) {
        $('#views').empty()

        var div = $('<div></div>').addClass('form-group');
            select = $('<select></select>').addClass('form-control'),
            label = $('<label></label>').attr('for', 'titles').addClass('control-label'),

        label.html(dataviva.dictionary['views']);

        for(view in views){
            option = $('<option value="'+view+'">'+view+'</option>')
            select.append(option);
        }

        div.append(label).append(select);
        $('#views').append(div);
    }

    function setGraphs(graphs) {
        $('#graphs').empty()

        var div = $('<div></div>').attr('class', 'dropdown dropdown-select');
            graphButton = $('<button data-toggle="dropdown" aria-expanded="true"></button>')
                            .attr('id', 'graph-button')
                            .attr('class', 'btn btn-outline btn-block dropdown-toggle'),
            dropDownMenu = $('<ul role="menu" aria-labelledby="graph-button"></ul>')
                            .attr('class', 'dropdown-menu'),
            label = $('<label></label>').attr('for', 'graph-button').addClass('control-label');

        label.html(dataviva.dictionary['graphs']);

        for(graph in graphs){
            option = $('<option value="'+graph+'">'+graph+'</option>')
            select.append(option);
        }

        div.on( 'click', '.dropdown-menu li a', function() {
           var target = $(this).html();

           //Adds active class to selected item
           $(this).parents('.dropdown-menu').find('li').removeClass('active');
           $(this).parent('li').addClass('active');

           //Displays selected text on dropdown-toggle button
           $(this).parents('.dropdown-select').find('.dropdown-toggle').html(target);
        });

        div.append(label).append(select);
        $('#graphs').append(div);
    }

    function updateViews() {
        $.ajax({
            method: "GET",
            url: "/" + lang + "/build_graph/views/" + dataset +"/" +
                $('#dimensions #filter0').val() + "/" +
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

    function changeDataSet() {
        buildGraph.dataset = this.value;
        setDimensions(dataviva.datasets[this.value].dimensions);
        updateViews();
    }

    function init() {
        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').on('change', changeDataSet);
    }
})();


$(document).ready(function () {
    dataviva.requireAttrs(['datasets'], function() {
        buildGraph.init();
    });
});


