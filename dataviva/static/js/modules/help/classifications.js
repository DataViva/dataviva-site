window.showLocations = function() {
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

    var loadingLocations = dataviva.ui.loading('.classifications-locations .classifications-locations-wrapper');
    loadingLocations.text(dataviva.dictionary['loading'] + "...");

    var LocationsTable = function () {
        this.tableId = '#locations-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-locations-control">frtip',
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
            "scrollCollapse": false,
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

                $('.classifications-locations-content .classifications-locations-control').append(buttons);

                $('#location-wages-table_filter input').removeClass('input-sm');
                $('#location-wages-table_filter').addClass('pull-right');
                $('#location-wages-states').addClass('active');

                $('#location-wages-regions').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/bra/?depth=1").load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#location-wages-states').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/bra/?depth=3").load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#location-wages-mesoregions').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/bra/?depth=5").load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#location-wages-microregions').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/bra/?depth=7").load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#location-wages-municipalities').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/bra/?depth=9").load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                loadingLocations.hide();
                $('.classifications-locations .classifications-locations-wrapper .classifications-locations-content').show();
            }
        });
    };
    window.locations = new LocationsTable(loadingLocations.hide());
};

window.showIndustries = function() {
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

    var loadingIndustries = dataviva.ui.loading('.classifications-industries .classifications-industries-wrapper');
    loadingIndustries.text(dataviva.dictionary['loading'] + "...");

    var IndustriesTable = function () {
        this.tableId = '#industries-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-industries-control">frtip',
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
            "scrollCollapse": false,
            "scroller": true,
            initComplete: function () {
                var buttons = $("<div></div>").addClass("btn-group");

                var cnae_1 = dataviva.dictionary['cnae_1'],
                    cnae_3 = dataviva.dictionary['cnae_3'],
                    cnae_6 = dataviva.dictionary['cnae_6'];

                buttons.append($("<button>"+cnae_1+"</button>").attr("id", 'industry-section').addClass("btn btn-white"));
                buttons.append($("<button>"+cnae_3+"</button>").attr("id", 'industry-division').addClass("btn btn-white"));
                buttons.append($("<button>"+cnae_6+"</button>").attr("id", 'industry-class').addClass("btn btn-white"));

                $('.classifications-industries-content .classifications-industries-control').append(buttons);

                $('#industry-table_filter input').removeClass('input-sm');
                $('#industry-table_filter').addClass('pull-right');
                $('#industry-section').addClass('active');

                $('#industry-section').click(function() {
                    loadingIndustries.show();
                    industries.table.ajax.url("/attrs/cnae/?depth=1").load(loadingIndustries.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#industry-division').click(function() {
                    loadingIndustries.show();
                    industries.table.ajax.url("/attrs/cnae/?depth=3").load(loadingIndustries.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#industry-class').click(function() {
                    loadingIndustries.show();
                    industries.table.ajax.url("/attrs/cnae/?depth=6").load(loadingIndustries.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                loadingIndustries.hide();
                $('.classifications-industries .classifications-industries-wrapper .classifications-industries-content').show();
            }
        });
    };
    window.industries = new IndustriesTable(loadingIndustries.hide());
};

$(document).ready(function () {
    $('a[data-toggle="tab"]').on('shown.bs.tab', function (e) {
        if (this.href.split('#')[1] === "tab-classifications"){
            if(!window.locations && !window.industries){
                dataviva.requireAttrs(['bra'], function() {
                    showLocations();
                });
                dataviva.requireAttrs(['cnae'], function() {
                    showIndustries();
                });
            }
        }
    });
});