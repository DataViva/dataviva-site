var TradePartnerTable = function () {
    this.tableId = '#trade-partner-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/secex/all-0/all/all/show.5/?order=export_val.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null,
            { "bVisible": false },
            null,
            null,
            { "bVisible": false },
            { "bVisible": false },
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

            tradePartnerTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               tradePartnerTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var tradePartnerTable = new TradePartnerTable();

var tradePartnerCountries = function() {
    tradePartnerTable.table.ajax.url("/secex/all-0/all/all/show.5/?order=eci.desc").load();
};

var tradePartnerContinents = function() {
    tradePartnerTable.table.ajax.url("/secex/all-0/all/all/show.2/?order=export_val.desc").load();
};

$(document).ready(function(){

    $('#trade-partner-countries').click(function() {
        tradePartnerCountries();
    });

    $('#trade-partner-continents').click(function() {
        tradePartnerContinents();
    });

});