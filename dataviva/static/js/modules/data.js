var data = {}
var count = 0;
$('#message').hide();
data.downloadLink = function() {
    dataSelection = []
    dataSelection.push($('#datasets').val());
    dataSelection.push($('select[name=year]').val());
    dataSelection.push($('#monthly-detail select').val());

    $('#dimensions select').each(function() {
        dataSelection.push(this.value);
    });

    dataSelection = dataSelection.filter(function(n){ return n != "" && n !== null && n != "all" });
    return dataviva.s3_host + "/data-download/" + lang + "/" + dataSelection.join("-") + '.csv.bz2';
}


$(document).ready(function() {
    $("#download").prop('disabled', true);
    $("#download").on('click', function() {
        window.open(data.downloadLink());
    });

    dataviva.requireAttrs(['datasets'], function() {
        for (dataset in dataviva.datasets) {
            $('#datasets').append( $('<option value="'+dataset+'">'+dataviva.dictionary[dataset]+'</option>'));
        }

        $('#datasets').on('change', function() {
            $("#download").prop('disabled', true);
            $('#datasets #dataset-empty-option').remove();
            $('#message').show();
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
                if (dimension.depths.length > 0){ 
                    var div = $("<div></div>").addClass("form-group col-md-4"),
                        label = $("<label></label>").attr("for", dimension.id).addClass("control-label"),
                        select = $("<select></select>").attr("id", dimension.id).addClass("form-control");

                    label.html(dataviva.dictionary[dimension.id + '_plural']);

                    $('#dimensions').append(div.append(label).append(select));

                    select.append($('<option value="all">'+dataviva.dictionary['all']+'</option>'));
                    dimension.depths.forEach(function(depth) {
                        select.append($('<option value="'+depth.value+'">'+dataviva.dictionary[depth.id]+'</option>'));
                    });
                }
            });

            $('#dimensions select').on('change', function (e) { 
                if ($(this).val() != "all") {
                    $("#download").prop('disabled', false);
                } 

                $('#dimensions select').each( function() {
                    if ($(this).val() == "all") count += 1;
                    if (count == $('#dimensions select').length) {
                        $("#download").prop('disabled', true);
                    }
                });
                count = 0;
            });
        });
    });
});
