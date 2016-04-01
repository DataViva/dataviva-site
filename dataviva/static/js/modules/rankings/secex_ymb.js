var SecexYmbTable = function () {
    this.tableId = '#secex-ymb-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/secex/all-0/show.3/all/all/?order=eci.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
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
            { "bVisible": false },
            { "bVisible": false },
            null,
            null,
            null,
            null
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $('#year-selector select')

            secexYmbTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               secexYmbTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var secexYmbTable = new SecexYmbTable();

var secexYmbStates = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.3/all/all/?order=eci.desc").load();
};

var secexYmbMunicipality = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.9/all/all/?order=eci.desc").load();
};

$(document).ready(function(){

    $('#secex-ymb-states').click(function() {
        secexYmbStates();
    });

    $('#secex-ymb-municipality').click(function() {
        secexYmbMunicipality();
    });

});

