var data = {}
$('#message').hide();
data.downloadLink = function () {
    dataSelection = []
    dataSelection.push($('#datasets').val());
    dataSelection.push($('select[name=year]').val());
    /*  dataSelection.push($('#monthly-detail select').val());
 
     $('#dimensions select').each(function() {
         dataSelection.push(this.value);
     }); */

    dataSelection = dataSelection.filter(function (n) { return n != "" && n !== null && n != "all" });
    return dataviva.s3_host + "/data-download/" + dataSelection[0] + "/" + lang + "/" + dataSelection.join("-") + '.csv.bz2';
}


$(document).ready(function () {
    $("#download").prop('disabled', true);
    $("#download").on('click', function () {
        window.open(data.downloadLink());
    });

    dataviva.requireAttrs(['datasets'], function () {
        $('#datasets').append($('<option value="rais">' + dataviva.dictionary["rais"] + '</option>'));
        $('#datasets').append($('<option value="secex">' + dataviva.dictionary["secex"] + '</option>'));
        $("#download").prop('disabled', true);

        $('#datasets').on('change', function () {
            $('#datasets #dataset-empty-option').remove();
            $('#message').show();

            /* if(this.value == 'secex') {
                $('#monthly-detail').show();
                $('#monthly-detail select').prop('disabled', false);

            } else {
                $('#monthly-detail').hide();
                $('#detailing').val('');
            }
 */
            $('select[name=year]').empty().prop('disabled', false);
            $("#download").prop('disabled', false);

           /*  for (let i = 2003; i < 2022; i++) {
                if (this.value = 'secex' && (i < 2021 && i > 2005)) {
                    $('select[name=year]').append($('<option value="' + i + '">' + i + '</option>'));
                } else {
                    $('select[name=year]').append($('<option value="' + i + '">' + i + '</option>'));
                }
            } */

            dataviva.datasets[this.value].years.forEach(function (year) {
                $('select[name=year]').append($('<option value="' + year + '">' + year + '</option>'));
            });

            /*  $('#dimensions').empty();
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
             }); */
        });
    });
});
