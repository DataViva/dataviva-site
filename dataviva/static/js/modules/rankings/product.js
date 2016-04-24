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
            null,
            {data: 14},
            {data: 15},
            {data: 3},
            {data: 2},
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
                    return dataviva.hs[row[16]].name
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
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['hs'], function() {
        window.product = new ProductTable();
    });
});

