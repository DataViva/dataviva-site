var LocationTradeRanking = function () {
    this.tableId = '#location-international-trade-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/secex/all-0/show.9/all/all/?order=eci.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            null,
            null,
            {data: 2},
            {data: 3},
            {data: 14},
            {data: 8},
            {data: 9},
            {data: 6},
            {data: 7},
            {data: 12},
            {data: 13},
            {data: 10},
            {data: 11},

        ],
        "columnDefs": [
            {
                "targets": 1,
                "render": function (data, type, row, meta){
                    if (dataviva.bra[row[15]].id_ibge === false){
                        return '-'
                    }
                    else {
                        return dataviva.bra[row[15]].id_ibge
                    }
                }
            },
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.bra[row[15]].name
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
                locationTradeRanking.table.ajax.url("/secex/all-0/show.1/all/all/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-states').click(function() {
                locationTradeRanking.table.ajax.url("/secex/all-0/show.3/all/all/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-mesoregions').click(function() {
                locationTradeRanking.table.ajax.url("/secex/all-0/show.5/all/all/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-microregions').click(function() {
                locationTradeRanking.table.ajax.url("/secex/all-0/show.7/all/all/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-international-trade-municipalities').click(function() {
                locationTradeRanking.table.ajax.url("/secex/all-0/show.9/all/all/?order=eci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
        }
    });
};

dataviva.requireAttrs(['bra'], function() {
    window.locationTradeRanking = new LocationTradeRanking();
});
