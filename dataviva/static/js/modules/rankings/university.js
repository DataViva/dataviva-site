var universityTable = function () {
    this.tableId = '#university-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/show/all/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null,
            null,
            null,
            null,
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            null,
            null
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {

            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control");

            select.append( $('<option value="">Ano</option>') );
            $('.rankings-content .rankings-control').append(select);

            universityTable.table
                .column( 10 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               universityTable.table
                    .column( 10 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#university-table_filter input').removeClass('input-sm');
            $('#university-table_filter').addClass('pull-right');
        }
    });
};

var universityTable = new universityTable();
