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
  $(id).siblings("input").val("all").trigger('change');
}


dataviva.requireAttrs(['datasets'], function() {

    for (dataset in dataviva.datasets) {
        $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
    }

    $('#datasets').on('change', function() {
        $('#datasets #dataset-empty-option').remove();
        var dataset = this.value;

        $('#dimensions').empty();
        dataviva.datasets[dataset].dimensions.forEach(function(dimension, index) {
                var div = $("<div></div>").addClass("form-group"),
                label = $("<label></label>").attr("for", dimension.id).addClass("control-label"),
                deactivate_button = $("<button></button>").attr("for", dimension.id).addClass("btn btn-xs btn-white pull-right")
                                        .html(dataviva.dictionary['deactivate'])
                                        .attr("onclick", "deactivate_dimension_graph(this)"),
                selector_button = $("<button></button>").attr("id", dimension.id).addClass("btn btn-block btn-outline btn-primary")
                                        .attr("onclick", "select_dimension_graph(id);")
                                        .html(dataviva.dictionary['select']);

                filter = $("<input></input>").attr("type", "hidden").attr("name", dimension.id).attr("id", 'filter'+index).val('all');

                label.html(dataviva.dictionary[dimension.id]);
            
                filter.change(function() {
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
                                //('#titles').empty()

                                window.buildGraphViews = result.views;

                                if(result.views){
                                    
                                    $('#views').empty()

                                    var div = $("<div></div>").addClass("form-group");
                                        select = $("<select></select>").addClass("form-control"),
                                        label = $("<label></label>").attr("for", "titles").addClass("control-label"),
                                        
                                    label.html(dataviva.dictionary["views"]);

                                    for(view in result.views){
                                        option = $('<option value="'+view+'">'+view+'</option>')
                                        select.append(option);
                                    }

                                    select.on('change', function() {
                                        $('#graphs').empty()

                                        for (graph in buildGraphViews[this.value]) {
                                            var name = buildGraphViews[this.value][graph].name,
                                                url = buildGraphViews[this.value][graph].url
                                            graphButton = $('<a></a>').addClass('btn btn-primary')
                                                            .attr('href', "/" + dataviva.language + '/embed/' + url)
                                                            .attr('target', "graphs-frame-build-graphs")
                                                            .html(name);
                                            $('#graphs').append(graphButton);
                                        }
                                    });

                                    div.append(label).append(select);

                                    $('#views').append(div);
                            }
                        }
                    });

                });

                if (dimension.name == 'School') { 
                    div.append(filter)
                } else {
                    div.append(filter).append(label).append(deactivate_button).append(selector_button)
                }

                $('#dimensions').append(div);
        });
    });
});







