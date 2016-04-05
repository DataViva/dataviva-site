var OccupationTable = function () {
    this.tableId = '#occupation-table';

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
            var select = $('#year-selector')

            occupationTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               occupationTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var occupationTable = new OccupationTable();

var occupationFamilies = function() {
    occupationTable.table.ajax.url("/rais/all/all/all/show.1/?order=num_jobs.desc").load();
};

var occupationGroups = function() {
    occupationTable.table.ajax.url("/rais/all/all/all/show.4/?order=num_jobs.desc").load();
};

$(document).ready(function(){

    $('#occupation-families').click(function() {
        occupationFamilies();
    });

    $('#occupation-groups').click(function() {
        occupationGroups();
    });

});
