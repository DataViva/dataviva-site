var TradePartnerTable = function () {
    this.tableId = '#trade-partner-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/secex/all-0/all/all/show.5/?order=export_val.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            {data: 15},
            null,
            {data: 14},
            {data: 2},
            {data: 3},
            {data: 8},
            {data: 9},
            {data: 6},
            {data: 7},
            {data: 10},
            {data: 11},
            {data: 12},
            {data: 13}
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.wld[row[15]].name
                }
            },
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            var wld_2 = dataviva.dictionary['wld_2'],
                wld_5 = dataviva.dictionary['wld_5'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+wld_2+"</button>").attr("id", 'trade-partner-continents').addClass("btn btn-white"));
            buttons.append($("<button>"+wld_5+"</button>").attr("id", 'trade-partner-countries').addClass("btn btn-white"));

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
            $('#trade-partner-countries').addClass('active');

            $('#trade-partner-continents').click(function() {
                tradePartnerTable.table.ajax.url("/secex/all-0/all/all/show.2/?order=export_val.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#trade-partner-countries').click(function() {
                tradePartnerTable.table.ajax.url("/secex/all-0/all/all/show.5/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            tradePartnerTable.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['wld'], function() {
        window.tradePartnerTable = new TradePartnerTable();
    });
});

