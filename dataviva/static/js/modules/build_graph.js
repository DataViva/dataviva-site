var selectorGraphs = Selector()
    .callback(function(d){
        $('#'+selectorGraphs.type()).html(d.name);
        $('#dimensions input[name='+selectorGraphs.type()+']').val(d.id).trigger('change');
        $('#modal-selector').modal('hide');
    });

function select_dimension_graph(id) {
  d3.select("#modal-selector-content").call(selectorGraphs.type(id));
  $('#modal-selector').modal('show');
}

function deactivate_dimension_graph(id) {
  $(id).siblings("button").html('Select');
  $(id).siblings("input").val("").trigger('change');

}

var viewParameters = {};

var update_views = function() {
  viewParameters = {};
  $('#dimensions input').each(function(){
    viewParameters[this.name] = this.value;
  })
}


dataviva.requireAttrs(['datasets'], function() {

    for (dataset in dataviva.datasets) {
        $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
    }

    $('#datasets').on('change', function() {
        $('#datasets #dataset-empty-option').remove();

        $('#dimensions').empty();
        dataviva.datasets[this.value].dimensions.forEach(function(dimension) {
            var div = $("<div></div>").addClass("form-group"),
                label = $("<label></label>").attr("for", dimension.id).addClass("control-label"),
                deactivate_button = $("<button></button>").attr("for", dimension.id).addClass("btn btn-xs btn-white pull-right")
                                        .html(dataviva.dictionary['deactivate'])
                                        .attr("onclick", "deactivate_dimension_graph(this)"),
                selector_button = $("<button></button>").attr("id", dimension.id).addClass("btn btn-block btn-outline btn-primary")
                                        .attr("onclick", "select_dimension_graph(id);")
                                        .html(dataviva.dictionary['select']);

                filter = $("<input></input>").attr("type", "hidden").attr("name", dimension.id);

            label.html(dataviva.dictionary[dimension.id]);

            $('#dimensions').append(div.append(label).append(deactivate_button).append(selector_button).append(filter));
        
            filter.change(function() {
              update_views();
            });

        });
    });



});



