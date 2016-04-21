var universityTable = function () {
    this.tableId = '#university-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/show/all/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            null,
            {data: 0},
            {data: 1},
            {data: 2},
            {data: 3},
            {data: 4},
            {data: 5},
            {data: 6},
            {data: 7},
            {data: 8},
            {data: 9}
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.university[row[11]].name
                }
            },
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {

            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control");

            var year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));

            $('.rankings-content .rankings-control').append(select);

            universityTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               universityTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#university-table_filter input').removeClass('input-sm');
            $('#university-table_filter').addClass('pull-right');

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['university'], function() {
        window.universityTable = new universityTable();
    });
});
