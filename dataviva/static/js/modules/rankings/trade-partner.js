var headers = {
    0:  "year",
    1:  "month",
    2:  "import_val",
    3:  "export_val",
    4:  "import_kg",
    5:  "export_kg",
    6:  "import_val_growth",
    7:  "import_val_growth_5",
    8:  "export_val_growth",
    9:  "export_val_growth_5",
    10: "bra_diversity",
    11: "bra_diversity_eff",
    12: "hs_diversity",
    13: "hs_diversity_eff",
    14: "eci",
    15: "wld_id"
}

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
            {
                render: function (data, type, row, meta){
                    return dataviva.wld[row[15]].name
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[14], {"key": headers[14]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[2], {"key": headers[2]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[8], {"key": headers[8]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[9], {"key": headers[9]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[6], {"key": headers[6]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[7], {"key": headers[7]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[10], {"key": headers[10]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[11], {"key": headers[11]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[12], {"key": headers[12]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[13], {"key": headers[13]});
                }
            }
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

