var ProductTable = function () {
    this.tableId = '#product-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/secex/all-0/all/show.6/all/?order=pci.desc",
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
            { "bVisible": false }, //bra_diversity
            { "bVisible": false }, //bra_diversity_eff
            null, //wld_diversity
            null, //wld_diversity_eff
            { "bVisible": false }, //rca_wld
            null, //pci
            null //hs_id
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Seções</button>").attr("id", 'product-sections').addClass("btn btn-white"));
            buttons.append($("<button>Posições</button>").attr("id", 'product-postions').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            product.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               product.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#product-table_filter input').removeClass('input-sm');
            $('#product-table_filter').addClass('pull-right');


            $('#product-sections').click(function() {
                productSections();
            });

            $('#product-postions').click(function() {
                productPositions();
            });
        }
    });
};

var product = new ProductTable();

var productSections = function() {
    product.table.ajax.url("/secex/all-0/all/show.2/all/?order=export_val.desc").load();
};

var productPositions = function() {
    product.table.ajax.url("/secex/all-0/all/show.6/all/?order=pci.desc").load();
};
