var headers = {
    0: "id_ibge",
    1: "location",
    2: "year",
    3: "month",
    4: "import_val",
    5: "export_val",
    6: "import_kg",
    7: "export_kg",
    8: "import_val_growth",
    9: "import_val_growth_5",
    10: "export_val_growth",
    11: "export_val_growth_5",
    12: "wld_diversity",
    13: "wld_diversity_eff",
    14: "hs_diversity",
    15: "hs_diversity_eff",
    16: "eci",
    17: "bra_id",
    18: "distance_wld",
    19: "opp_gain_wld"
}

var loadingRankings = dataviva.ui.loading('.rankings .rankings-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var LocationTradeRanking = function () {
    this.tableId = '#location-international-trade-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">Bfrtip',
        "buttons": [ 
            {
                extend: 'csvHtml5',
                text: '<i class="fa fa-floppy-o fa-lg"></i>',
                filename: 'rankings-location-international-trade'
            }
        ],
        "ajax": {
            "url": "/secex/all-0/show.9/all/all/?order=eci.desc",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {data: 2},
            {
                render: function (data, type, row, meta){
                    return row[0] === null ? '-' : row[0];
                }
            },
            {
                render: function (data, type, row, meta){
                    var abbreviation = dataviva.bra[row[19]].abbreviation;
                    return row[1].truncate(35) + (abbreviation ? " - " + abbreviation : "");
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[18], {"key": headers[16]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[5], {"key": headers[5]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[4], {"key": headers[4]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[12], {"key": headers[18]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[13], {"key": headers[19]});
                },
                className: "table-number",
                type: 'num-dataviva'
            }
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

            var bra_1 = dataviva.dictionary['bra_1'],
                bra_3 = dataviva.dictionary['bra_3'],
                bra_5 = dataviva.dictionary['bra_5'],
                bra_7 = dataviva.dictionary['bra_7'],
                bra_9 = dataviva.dictionary['bra_9'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+bra_1+"</button>").attr("id", 'location-international-trade-regions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_3+"</button>").attr("id", 'location-international-trade-states').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_5+"</button>").attr("id", 'location-international-trade-mesoregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_7+"</button>").attr("id", 'location-international-trade-microregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_9+"</button>").attr("id", 'location-international-trade-municipalities').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            locationTradeRanking.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               locationTradeRanking.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#location-international-trade-table_filter input').removeClass('input-sm');
            $('#location-international-trade-table_filter').addClass('pull-right');
            $('#location-international-trade-municipalities').addClass('active');

            $('#location-international-trade-regions').click(function() {
                loadingRankings.show();
                locationTradeRanking.table.ajax.url("/secex/all-0/show.1/all/all/?order=eci.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-states').click(function() {
                loadingRankings.show();
                locationTradeRanking.table.ajax.url("/secex/all-0/show.3/all/all/?order=eci.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-mesoregions').click(function() {
                loadingRankings.show();
                locationTradeRanking.table.ajax.url("/secex/all-0/show.5/all/all/?order=eci.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-microregions').click(function() {
                loadingRankings.show();
                locationTradeRanking.table.ajax.url("/secex/all-0/show.7/all/all/?order=eci.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-municipalities').click(function() {
                loadingRankings.show();
                locationTradeRanking.table.ajax.url("/secex/all-0/show.9/all/all/?order=eci.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            locationTradeRanking.table
                    .column(0)
                    .search(lastYear)
                    .draw();

            loadingRankings.hide();
            $('.rankings .rankings-wrapper .rankings-content').show();
        }
    });
};

dataviva.requireAttrs(['bra'], function() {
    window.locationTradeRanking = new LocationTradeRanking();
});
