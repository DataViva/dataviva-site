var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "gender",
    4: "icon",
    5: "id",
    6: "img_author",
    7: "img_link",
    8: "keywords",
    9: "name",
    10: "num_jobs",
    11: "plural_pt",
    12: "url"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var OccupationsTable = function () {
    this.tableId = '#occupations-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/cbo/?depth=4",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {"data": "id"},
            {
                render: function (data, type, row, meta){
                    return dataviva.cbo[(row.id)].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.num_jobs, {"key": headers[10]});
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

            var cbo_1 = dataviva.dictionary['cbo_1'],
                cbo_4 = dataviva.dictionary['cbo_4'];

            buttons.append($("<button>"+cbo_1+"</button>").attr("id", 'occupations-groups').addClass("btn btn-white"));
            buttons.append($("<button>"+cbo_4+"</button>").attr("id", 'occupations-families').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#occupations-table_filter input').removeClass('input-sm');
            $('#occupations-table_filter').addClass('pull-right');
            $('#occupations-families').addClass('active');

            $('#occupations-groups').click(function() {
                loadingRankings.show();
                occupations.table.ajax.url("/attrs/cbo/?depth=1").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#occupations-families').click(function() {
                loadingRankings.show();
                occupations.table.ajax.url("/attrs/cbo/?depth=4").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['cbo'], function() {
    window.occupations = new OccupationsTable(loadingRankings.hide);
});
