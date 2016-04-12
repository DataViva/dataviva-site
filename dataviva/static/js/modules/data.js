$(document).ready(function() {
    $.ajax({
        url: 'databases',
        dataType: 'json',
    })
    .done(function(databases) {

        for (database in databases) {
            $('#databases').append( $('<option value="'+database+'">'+dataviva.dictionary[database]+'</option>'));
        }

    });

    $('#databases').on('change', function() {
        $('#databases #database-empty-option').remove();
        console.log(this.value);
    });
});