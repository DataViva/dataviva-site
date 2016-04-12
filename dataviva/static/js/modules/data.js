var data = {}
data.downloadLink = function() {
    dataSelection = []
    dataSelection.push($('#databases').val());
    dataSelection.push($('select[name=year]').val());
    dataSelection.push($('#monthly-detail select').val());

    $('#dimensions select').each(function() {
        dataSelection.push(this.value);
    });

    dataSelection = dataSelection.filter(function(n){ return n != "" && n !== null && n != "all" });
    return "https://dataviva.s3.amazonaws.com/download/" + dataSelection.join("-") + '.csv.bz2';
}

$(document).ready(function() {


    $.ajax({
        url: 'databases',
        dataType: 'json',
    })
    .done(function(databases) {

        for (database in databases) {
            $('#databases').append( $('<option value="'+database+'">'+dataviva.dictionary[database]+'</option>'));
        }

        $('#databases').on('change', function() {
            $('#databases #database-empty-option').remove();

            if(this.value == 'secex') {
                $('#monthly-detail').show();
                $('#monthly-detail select').prop('disabled', false);

            } else {
                $('#detailing').val('anual');
                $('#monthly-detail').hide();
            }

            $('select[name=year]').empty().prop('disabled', false);;

            databases[this.value].years.forEach(function(year) {
                $('select[name=year]').append($('<option value="'+year+'">'+year+'</option>'));
            });

            $('#dimensions').empty();
            databases[this.value].dimensions.forEach(function(dimension) {

                var div = $("<div></div>").addClass("form-group col-md-4"),
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