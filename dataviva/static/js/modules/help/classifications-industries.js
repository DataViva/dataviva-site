var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "gender",
    4: "icon",
    5: "id",
    6: "keywords",
    7: "name",
    8: "num_jobs",
    9: "plural_pt",
    10: "url"
};

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var LocationsTable = function () {
    this.tableId = '#industries-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/cnae/?depth=1",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            
            {
                render: function (data, type, row, meta){
                    if (row.id){
                        return row.id.toUpperCase();
                    }
                    else{
                        return '-'
                    }
                },
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.cnae[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.num_jobs, {"key": headers[8]});
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

            var cnae_1 = dataviva.dictionary['cnae_1'],
                cnae_3 = dataviva.dictionary['cnae_3'],
                cnae_6 = dataviva.dictionary['cnae_6'];

            buttons.append($("<button>"+cnae_1+"</button>").attr("id", 'industry-section').addClass("btn btn-white"));
            buttons.append($("<button>"+cnae_3+"</button>").attr("id", 'industry-division').addClass("btn btn-white"));
            buttons.append($("<button>"+cnae_6+"</button>").attr("id", 'industry-class').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#industry-table_filter input').removeClass('input-sm');
            $('#industry-table_filter').addClass('pull-right');
            $('#industry-states').addClass('active');

            $('#industry-section').click(function() {
                loadingRankings.show();
                industries.table.ajax.url("/attrs/cnae/?depth=1").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#industry-division').click(function() {
                loadingRankings.show();
                industries.table.ajax.url("/attrs/cnae/?depth=3").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#industry-class').click(function() {
                loadingRankings.show();
                industries.table.ajax.url("/attrs/cnae/?depth=6").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['cnae'], function() {
    window.industries = new LocationsTable(loadingRankings.hide);
});
