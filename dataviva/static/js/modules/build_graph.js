var dimensionSelectCallback = function(id, event) {
    $('#'+id).html(d.name);
    $('#modal-selector').modal('hide');
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
                                        .html(dataviva.dictionary['deactivate']),
                selector_button = $("<button></button>").attr("id", dimension.id).addClass("btn btn-block btn-outline btn-white")
                                        .attr("onclick", "select_attr(id);")
                                        .html(dataviva.dictionary['select']);

            label.html(dataviva.dictionary[dimension.id]);

            $('#dimensions').append(div.append(label).append(deactivate_button).append(selector_button));
        });
    });
});
