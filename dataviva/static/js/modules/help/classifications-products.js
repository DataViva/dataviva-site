var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "export_val",
    4: "gender",
    5: "icon",
    6: "id",
    7: "img_author",
    8: "img_link",
    9: "keywords",
    10: "name",
    11: "plural_pt",
    12: "url"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var ProductsTable = function () {
    this.tableId = '#products-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/hs/?depth=2",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {"data": "id"},
            {
                render: function (data, type, row, meta){
                    return dataviva.hs[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.export_val, {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {"data": "color"},
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var buttons = $("<div></div>").addClass("btn-group");

            var hs_2 = dataviva.dictionary['hs_2'],
                hs_6 = dataviva.dictionary['hs_6'];

            buttons.append($("<button>"+hs_2+"</button>").attr("id", 'products-sections').addClass("btn btn-white"));
            buttons.append($("<button>"+hs_6+"</button>").attr("id", 'products-postions').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#products-table_filter input').removeClass('input-sm');
            $('#products-table_filter').addClass('pull-right');
            $('#products-sections').addClass('active');


            $('#products-sections').click(function() {
                loadingRankings.show();
                products.table.ajax.url("/attrs/hs/?depth=2").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#products-postions').click(function() {
                loadingRankings.show();
                products.table.ajax.url("/attrs/hs/?depth=6").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['hs'], function() {
    window.products = new ProductsTable(loadingRankings.hide);
});
