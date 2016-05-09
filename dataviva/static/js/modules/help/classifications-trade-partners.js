var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "export_val",
    4: "gender",
    5: "icon",
    6: "id",
    7: "id_2char",
    8: "id_3char",
    9: "id_mdic",
    10: "id_num",
    11: "keywords",
    12: "name",
    13: "plural_pt",
    14: "url",
};

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var LocationsTable = function () {
    this.tableId = '#tradePartners-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/wld/?depth=2",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                    return row.id.toUpperCase()
                    }
            },
            {
                render: function (data, type, row, meta){
                    
                    if (row.id_mdic){
                        return row.id_mdic;
                    }
                    else{
                        return '-'
                    }
                },
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.wld[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.export_val, {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {"data": "color"}
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var buttons = $("<div></div>").addClass("btn-group");

            var wld_2 = dataviva.dictionary['wld_2'],
                wld_5 = dataviva.dictionary['wld_5' ];

            buttons.append($("<button>"+wld_2+"</button>").attr("id", 'tradePartner-continent').addClass("btn btn-white"));
            buttons.append($("<button>"+wld_5+"</button>").attr("id", 'tradePartner-country').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#tradePartner-table_filter input').removeClass('input-sm');
            $('#tradePartner-table_filter').addClass('pull-right');
            $('#tradePartner-continent').addClass('active');

            $('#tradePartner-continent').click(function() {
                loadingRankings.show();
                tradePartner.table.ajax.url("/attrs/wld/?depth=2").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#tradePartner-country').click(function() {
                loadingRankings.show();
                tradePartner.table.ajax.url("/attrs/wld/?depth=5").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['wld'], function() {
    window.tradePartner = new LocationsTable(loadingRankings.hide);
});
