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
            var select = $('#year-selector')

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

var wagesRegions = function() {
    wagesTable.table.ajax.url("/rais/all/show.1/all/all/?order=num_jobs.desc").load();
};

var wagesStates = function() {
    wagesTable.table.ajax.url("/rais/all/show.3/all/all/?order=num_jobs.desc").load();
};

var wagesMesoregions = function() {
    wagesTable.table.ajax.url("/rais/all/show.5/all/all/?order=num_jobs.desc").load();
};

var wagesMicroregions = function() {
    wagesTable.table.ajax.url("/rais/all/show.7/all/all/?order=num_jobs.desc").load();
};

var wagesMunicipalities = function() {
    wagesTable.table.ajax.url("/rais/all/show.9/all/all/?order=num_jobs.desc").load();
};

$(document).ready(function(){

    $('#location-wages-regions').click(function() {
        wagesRegions();
    });

    $('#location-wages-states').click(function() {
        wagesStates();
    });

    $('#location-wages-mesoregions').click(function() {
        wagesMesoregions();
    });

    $('#location-wages-microregions').click(function() {
        wagesMicroRegions();
    });

    $('#location-wages-municipalities').click(function() {
        wagesMunicipalities();
    });

});
