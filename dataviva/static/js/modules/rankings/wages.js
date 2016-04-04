var WagesTable = function () {
    this.tableId = '#wages-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/rais/all/show.3/all/all/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null,
            null,
            null,
            null,
            null,
            null,
            null,
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            null,
            null,
            null,
            null,
            null,
            { "bVisible": false },
            null
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $('#year-selector select')

            wagesTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               wagesTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var wagesTable = new WagesTable();

var wagesStates = function() {
    wagesTable.table.ajax.url("/rais/all/show.3/all/all/?order=num_jobs.desc").load();
};

var wagesMunicipality = function() {
    wagesTable.table.ajax.url("/rais/all/show.9/all/all/?order=num_jobs.desc").load();
};

$(document).ready(function(){

    $('#wages-states').click(function() {
        wagesStates();
    });

    $('#wages-municipality').click(function() {
        wagesMunicipality();
    });

});
