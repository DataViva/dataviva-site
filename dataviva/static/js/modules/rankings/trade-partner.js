var LocationInternationalTradeTable = function () {
    this.tableId = '#location-international-trade-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/secex/all-0/all/all/show.5/?order=export_val.desc",
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

            locationInternationalTradeTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               locationInternationalTradeTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var locationInternationalTradeTable = new LocationInternationalTradeTable();

var locationInternationalTradeRegions = function() {
    locationInternationalTradeTable.table.ajax.url("/secex/all-0/show.1/all/all/?order=eci.desc").load();
};

var locationInternationalTradeStates = function() {
    locationInternationalTradeTable.table.ajax.url("/secex/all-0/show.3/all/all/?order=eci.desc").load();
};

var locationInternationalTradeMesoregions = function() {
    locationInternationalTradeTable.table.ajax.url("/secex/all-0/show.5/all/all/?order=eci.desc").load();
};

var locationInternationalTradeMicroRegions = function() {
    locationInternationalTradeTable.table.ajax.url("/secex/all-0/show.7/all/all/?order=eci.desc").load();
};

var locationInternationalTradeMunicipalities = function() {
    locationInternationalTradeTable.table.ajax.url("/secex/all-0/show.9/all/all/?order=eci.desc").load();
};

$(document).ready(function(){

    $('#location-international-trade-regions').click(function() {
        locationInternationalTradeStates();
    });

    $('#location-international-trade-states').click(function() {
        locationInternationalTradeStates();
    });

    $('#location-international-trade-mesoregions').click(function() {
        locationInternationalTradeMesoregions();
    });

    $('#location-international-trade-microregions').click(function() {
        locationInternationalTradeMicroRegions();
    });

    $('#location-international-trade-municipalities').click(function() {
        locationInternationalTradeMunicipalities();
    });

});