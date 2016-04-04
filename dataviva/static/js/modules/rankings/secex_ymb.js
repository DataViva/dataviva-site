var SecexYmbTable = function () {
    this.tableId = '#secex-ymb-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/secex/all-0/show.1/all/all/?order=eci.desc",
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
            var select = $('#year-selector')

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

var secexYmbRegions = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.1/all/all/?order=eci.desc").load();
};

var secexYmbStates = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.3/all/all/?order=eci.desc").load();
};

var secexYmbMesoregions = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.5/all/all/?order=eci.desc").load();
};

var secexYmbMicroRegions = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.7/all/all/?order=eci.desc").load();
};

var secexYmbMunicipalities = function() {
    secexYmbTable.table.ajax.url("/secex/all-0/show.9/all/all/?order=eci.desc").load();
};

$(document).ready(function(){

    $('#secex-ymb-regions').click(function() {
        secexYmbStates();
    });

    $('#secex-ymb-states').click(function() {
        secexYmbStates();
    });

    $('#secex-ymb-mesoregions').click(function() {
        secexYmbMesoregions();
    });

    $('#secex-ymb-microregions').click(function() {
        secexYmbMicroRegions();
    });

    $('#secex-ymb-municipalities').click(function() {
        secexYmbMunicipalities();
    });

});

