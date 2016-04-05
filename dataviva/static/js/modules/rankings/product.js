var ProductTable = function () {
    this.tableId = '#product-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/secex/all-0/all/show.6/all/?order=pci.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //year
            null, //month
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
            var select = $('#year-selector')

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

            $('#year-selector').append(select);
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

$(document).ready(function(){

    $('#product-sections').click(function() {
        productSections();
    });

    $('#product-postions').click(function() {
        productPositions();
    });

});
