$(document).ready(function() {

    $.ajax({
        url: 'datasets',
        dataType: 'json',
    })
    .done(function(datasets) {

        for (dataset in datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').on('change', function() {
            $('#datasets #dataset-empty-option').remove();

            $('#dimensions').empty();
            datasets[this.value].dimensions.forEach(function(dimension) {

                var div = $("<div></div>").addClass("form-group"),
                    label = $("<label></label>").attr("for", dimension.name).addClass("control-label"),
                    select = $("<select></select>").attr("id", dimension.name).addClass("form-control");

                label.html(dataviva.dictionary[dimension.id]);

                $('#dimensions').append(div.append(label).append(select));

                select.append($('<option value="all">'+dataviva.dictionary['all']+'</option>'));
                dimension.depths.forEach(function(depth) {
                    select.append($('<option value="'+depth.value+'">'+dataviva.dictionary[depth.id]+'</option>'));
                });
            });
        });
    });
});