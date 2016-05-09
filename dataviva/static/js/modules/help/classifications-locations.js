var headers = {
    0: "abbreviation",
    1: "article",
    2: "color",
    3: "desc",
    4: "gender",
    5: "icon",
    6: "id",
    7: "id_ibge",
    8: "keywords",
    9: "name",
    10: "plural_pt",
    11: "population",
    12: "url"
};

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var LocationsTable = function () {
    this.tableId = '#locations-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/bra/?depth=3",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                    return row.id.toUpperCase();
                }
            },
            {
                render: function (data, type, row, meta){
                    if (row.id_ibge){
                        return row.id_ibge;
                    }
                    else{
                        return '-'
                    }
                },
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.bra[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.population, {"key": headers[11]});
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

            var bra_1 = dataviva.dictionary['bra_1'],
                bra_3 = dataviva.dictionary['bra_3'],
                bra_5 = dataviva.dictionary['bra_5'],
                bra_7 = dataviva.dictionary['bra_7'],
                bra_9 = dataviva.dictionary['bra_9'];

            buttons.append($("<button>"+bra_1+"</button>").attr("id", 'location-wages-regions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_3+"</button>").attr("id", 'location-wages-states').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_5+"</button>").attr("id", 'location-wages-mesoregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_7+"</button>").attr("id", 'location-wages-microregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_9+"</button>").attr("id", 'location-wages-municipalities').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#location-wages-table_filter input').removeClass('input-sm');
            $('#location-wages-table_filter').addClass('pull-right');
            $('#location-wages-states').addClass('active');

            $('#location-wages-regions').click(function() {
                loadingRankings.show();
                locations.table.ajax.url("/attrs/bra/?depth=1").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-states').click(function() {
                loadingRankings.show();
                locations.table.ajax.url("/attrs/bra/?depth=3").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-mesoregions').click(function() {
                loadingRankings.show();
                locations.table.ajax.url("/attrs/bra/?depth=5").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-microregions').click(function() {
                loadingRankings.show();
                locations.table.ajax.url("/attrs/bra/?depth=7").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-municipalities').click(function() {
                loadingRankings.show();
                locations.table.ajax.url("/attrs/bra/?depth=9").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['bra'], function() {
    window.locations = new LocationsTable(loadingRankings.hide);
});
