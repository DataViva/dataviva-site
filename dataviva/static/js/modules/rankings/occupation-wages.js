var OccupationWagesTable = function () {
    this.tableId = '#occupation-wages-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/rais/all/all/all/show.1/?order=num_jobs.desc",
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
            null,
            null,
            null,
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
            var select = $('#year-selector')

            occupationWagesTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               occupationWagesTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var occupationWagesTable = new OccupationWagesTable();

var occupationWagesFamilies = function() {
    occupationWagesTable.table.ajax.url("/rais/all/all/all/show.1/?order=num_jobs.desc").load();
};

var occupationWagesGroups = function() {
    occupationWagesTable.table.ajax.url("/rais/all/all/all/show.4/?order=num_jobs.desc").load();
};

$(document).ready(function(){

    $('#occupation-wages-families').click(function() {
        occupationWagesFamilies();
    });

    $('#occupation-wages-groups').click(function() {
        occupationWagesGroups();
    });

});
