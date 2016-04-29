var data = {}
data.downloadLink = function() {
    dataSelection = []
    dataSelection.push($('#datasets').val());
    dataSelection.push($('select[name=year]').val());
    dataSelection.push($('#monthly-detail select').val());

    $('#dimensions select').each(function() {
        dataSelection.push(this.value);
    });

    dataSelection = dataSelection.filter(function(n){ return n != "" && n !== null && n != "all" });
    return "https://dataviva.s3.amazonaws.com/data-download/"+lang+"/" + dataSelection.join("-") + '.csv.bz2';
}


$(document).ready(function() {

    $("#download").on('click', function() {
        window.open(data.downloadLink());
    });

    dataviva.requireAttrs(['datasets'], function() {
        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').on('change', function() {
            $('#datasets #dataset-empty-option').remove();

            if(this.value == 'secex') {
                $('#monthly-detail').show();
                $('#monthly-detail select').prop('disabled', false);

            } else {
                $('#monthly-detail').hide();
                $('#detailing').val('');
            }

            $('select[name=year]').empty().prop('disabled', false);

            dataviva.datasets[this.value].years.forEach(function(year) {
                $('select[name=year]').append($('<option value="'+year+'">'+year+'</option>'));
            });

            $('#dimensions').empty();
            dataviva.datasets[this.value].dimensions.forEach(function(dimension) {

                var div = $("<div></div>").addClass("form-group col-md-4"),
                    label = $("<label></label>").attr("for", dimension.id).addClass("control-label"),
                    select = $("<select></select>").attr("id", dimension.id).addClass("form-control");

                label.html(dataviva.dictionary[dimension.id + '_plural']);

                $('#dimensions').append(div.append(label).append(select));

                select.append($('<option value="all">'+dataviva.dictionary['all']+'</option>'));
                dimension.depths.forEach(function(depth) {
                    select.append($('<option value="'+depth.value+'">'+dataviva.dictionary[depth.id]+'</option>'));
                });
            });
            $("#download").prop('disabled', false);
        });
    });
});
