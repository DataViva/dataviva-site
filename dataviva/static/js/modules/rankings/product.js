var headers = {
    0: "year",
    1: "month",
    2: "import_val",
    3: "export_val",
    4: "import_kg",
    5: "export_kg",
    6: "import_val_growth",
    7: "import_val_growth_5",
    8: "export_val_growth",
    9: "export_val_growth_5",
    10: "bra_diversity",
    11: "bra_diversity_eff",
    12: "wld_diversity",
    13: "wld_diversity_eff",
    14: "rca_wld",
    15: "pci",
    16: "hs_id"
}

var loadingRankings = dataviva.ui.loading('.rankings .rankings-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var ProductTable = function () {
    this.tableId = '#product-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/secex/all-0/all/show.6/all/?order=pci.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            {data: 16},
            {
                render: function (data, type, row, meta){
                    return dataviva.hs[row[16]].name.truncate(35);
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[14], {"key": headers[14]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[15], {"key": headers[15]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[2], {"key": headers[2]});
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
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            var hs_2 = dataviva.dictionary['hs_2'],
                hs_6 = dataviva.dictionary['hs_6'],
                year = dataviva.dictionary['year'];

            select.append( $('<option value="">'+year+'</option>') );
            buttons.append($("<button>"+hs_2+"</button>").attr("id", 'product-sections').addClass("btn btn-white"));
            buttons.append($("<button>"+hs_6+"</button>").attr("id", 'product-postions').addClass("btn btn-white"));

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
            $('#product-postions').addClass('active');


            $('#product-sections').click(function() {
                product.table.ajax.url("/secex/all-0/all/show.2/all/?order=export_val.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#product-postions').click(function() {
                product.table.ajax.url("/secex/all-0/all/show.6/all/?order=pci.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            product.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();

            loadingRankings.hide();
            $('.rankings .rankings-wrapper .rankings-content').show();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['hs'], function() {
        window.product = new ProductTable();
    });
});

