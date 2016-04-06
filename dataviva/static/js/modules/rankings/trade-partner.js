var TradePartnerTable = function () {
    this.tableId = '#trade-partner-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
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
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Regiões</button>").attr("id", 'trade-partner-continents').addClass("btn btn-white"));
            buttons.append($("<button>Estados</button>").attr("id", 'trade-partner-countries').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

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

            $('#trade-partner-table_filter input').removeClass('input-sm');
            $('#trade-partner-table_filter').addClass('pull-right');

            $('#trade-partner-countries').click(function() {
                tradePartnerCountries();
            });

            $('#trade-partner-continents').click(function() {
                tradePartnerContinents();
            });
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
