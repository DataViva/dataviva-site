var LocationInternationalTradeTable = function () {
    this.tableId = '#location-international-trade-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/secex/all-0/show.1/all/all/?order=eci.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //year
            { "bVisible": false }, //month
            null, //import_val
            null, //export_val
            { "bVisible": false }, //import_kg
            { "bVisible": false }, //export_kg
            { "bVisible": false }, //import_val_growth
            { "bVisible": false }, //import_val_growth_5
            { "bVisible": false }, //export_val_growth
            { "bVisible": false }, //export_val_growth_5
            { "bVisible": false }, //wld_diversity
            { "bVisible": false }, //wld_diversity_eff
            null, //hs_diversity
            null, //hs_diversity_eff
            null, //eci
            null //bra_id
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Regiões</button>").attr("id", 'location-international-trade-regions').addClass("btn btn-white"));
            buttons.append($("<button>Estados</button>").attr("id", 'location-international-trade-states').addClass("btn btn-white"));
            buttons.append($("<button>Mesoregiões</button>").attr("id", 'location-international-trade-mesoregions').addClass("btn btn-white"));
            buttons.append($("<button>Microregiões</button>").attr("id", 'location-international-trade-microregions').addClass("btn btn-white"));
            buttons.append($("<button>Municípios</button>").attr("id", 'location-international-trade-municipalities').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

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

            $('#location-international-trade-table_filter input').removeClass('input-sm');
            $('#location-international-trade-table_filter').addClass('pull-right');

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
