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
            "dom": '<"classifications-locations-control">Bfrtip',
            "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-locations'
                }
            ],
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
                        try {
                            return dataviva.bra[row.id].name;
                        } catch (e) {
                            return row.name;
                        }
                    }
                },
                {
                    render: function (data, type, row, meta){
                        var population = dataviva.format.number(row.population, {"key": headers[11]});
                        return population == 'NaN' ? '-' : population;
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
                loadingLocations.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var bra_1 = dataviva.dictionary['bra_1'],
                    bra_3 = dataviva.dictionary['bra_3'],
                    bra_5 = dataviva.dictionary['bra_5'],
                    bra_7 = dataviva.dictionary['bra_7'],
                    bra_9 = dataviva.dictionary['bra_9'],
                    health_region = dataviva.dictionary['health_region'];

                buttons.append($("<button>"+bra_1+"</button>").attr("id", 'location-wages-regions').addClass("btn btn-white"));
                buttons.append($("<button>"+bra_3+"</button>").attr("id", 'location-wages-states').addClass("btn btn-white"));
                buttons.append($("<button>"+bra_5+"</button>").attr("id", 'location-wages-mesoregions').addClass("btn btn-white"));
                buttons.append($("<button>"+bra_7+"</button>").attr("id", 'location-wages-microregions').addClass("btn btn-white"));
                buttons.append($("<button>"+bra_9+"</button>").attr("id", 'location-wages-municipalities').addClass("btn btn-white"));
                buttons.append($("<button>"+health_region+"</button>").attr("id", 'location-wages-health-region').addClass("btn btn-white"));

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

                $('#location-wages-health-region').click(function() {
                    loadingLocations.show();
                    locations.table.ajax.url("/attrs/health_region/?lang=" + lang).load(loadingLocations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-locations .classifications-locations-wrapper .classifications-locations-content').show();
                loadingLocations.hide();
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
            "dom": '<"classifications-industries-control">Bfrtip',
            "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-industries'
                }
            ],
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
                        return dataviva.cnae[row.id].name.truncate(65);
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
                loadingIndustries.show();
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

                $('.classifications-industries .classifications-industries-wrapper .classifications-industries-content').show();
                loadingIndustries.hide();
            }
        });
    };
    window.industries = new IndustriesTable(loadingIndustries.hide());
};

window.showOccupations = function() {
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

    var loadingOccupations = dataviva.ui.loading('.classifications-occupations .classifications-occupations-wrapper');
    loadingOccupations.text(dataviva.dictionary['loading'] + "...");

    var OccupationsTable = function () {
        this.tableId = '#occupations-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-occupations-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-occupations'
                }
            ],
            "ajax": {
                "url": "/attrs/cbo/?depth=1",
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
                loadingOccupations.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var cbo_1 = dataviva.dictionary['cbo_1'],
                    cbo_4 = dataviva.dictionary['cbo_4'];

                buttons.append($("<button>"+cbo_1+"</button>").attr("id", 'occupations-groups').addClass("btn btn-white"));
                buttons.append($("<button>"+cbo_4+"</button>").attr("id", 'occupations-families').addClass("btn btn-white"));

                $('.classifications-occupations-content .classifications-occupations-control').append(buttons);

                $('#occupations-table_filter input').removeClass('input-sm');
                $('#occupations-table_filter').addClass('pull-right');
                $('#occupations-groups').addClass('active');

                $('#occupations-groups').click(function() {
                    loadingOccupations.show();
                    occupations.table.ajax.url("/attrs/cbo/?depth=1").load(loadingOccupations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#occupations-families').click(function() {
                    loadingOccupations.show();
                    occupations.table.ajax.url("/attrs/cbo/?depth=4").load(loadingOccupations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-occupations .classifications-occupations-wrapper .classifications-occupations-content').show();
                loadingOccupations.hide();
            }
        });
    };
    window.occupations = new OccupationsTable(loadingOccupations.hide());
};

window.showProducts = function() {
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

    var loadingProducts = dataviva.ui.loading('.classifications-products .classifications-products-wrapper');
    loadingProducts.text(dataviva.dictionary['loading'] + "...");

    var ProductsTable = function () {
        this.tableId = '#products-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-products-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-products'
                }
            ],
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
                loadingProducts.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var hs_2 = dataviva.dictionary['hs_2'],
                    hs_6 = dataviva.dictionary['hs_6'];

                buttons.append($("<button>"+hs_2+"</button>").attr("id", 'products-sections').addClass("btn btn-white"));
                buttons.append($("<button>"+hs_6+"</button>").attr("id", 'products-postions').addClass("btn btn-white"));

                $('.classifications-products-content .classifications-products-control').append(buttons);

                $('#products-table_filter input').removeClass('input-sm');
                $('#products-table_filter').addClass('pull-right');
                $('#products-sections').addClass('active');


                $('#products-sections').click(function() {
                    loadingProducts.show();
                    products.table.ajax.url("/attrs/hs/?depth=2").load(loadingProducts.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#products-postions').click(function() {
                    loadingProducts.show();
                    products.table.ajax.url("/attrs/hs/?depth=6").load(loadingProducts.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-products .classifications-products-wrapper .classifications-products-content').show();
                loadingProducts.hide();
            }
        });
    };
    window.products = new ProductsTable(loadingProducts.hide());
};

window.showTradePartners = function() {
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

    var loadingTradePartners = dataviva.ui.loading('.classifications-trade-partners .classifications-trade-partners-wrapper');
    loadingTradePartners.text(dataviva.dictionary['loading'] + "...");

    var TradePartnersTable = function () {
        this.tableId = '#trade-partners-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-trade-partners-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-trade-partners'
                }
            ],
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
                loadingTradePartners.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var wld_2 = dataviva.dictionary['wld_2'],
                    wld_5 = dataviva.dictionary['wld_5' ];

                buttons.append($("<button>"+wld_2+"</button>").attr("id", 'tradePartner-continent').addClass("btn btn-white"));
                buttons.append($("<button>"+wld_5+"</button>").attr("id", 'tradePartner-country').addClass("btn btn-white"));

                $('.classifications-trade-partners-content .classifications-trade-partners-control').append(buttons);

                $('#tradePartner-table_filter input').removeClass('input-sm');
                $('#tradePartner-table_filter').addClass('pull-right');
                $('#tradePartner-continent').addClass('active');

                $('#tradePartner-continent').click(function() {
                    loadingTradePartners.show();
                    tradePartners.table.ajax.url("/attrs/wld/?depth=2").load(loadingTradePartners.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#tradePartner-country').click(function() {
                    loadingTradePartners.show();
                    tradePartners.table.ajax.url("/attrs/wld/?depth=5").load(loadingTradePartners.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-trade-partners .classifications-trade-partners-wrapper .classifications-trade-partners-content').show();
                loadingTradePartners.hide();
            }
        });
    };
    window.tradePartners = new TradePartnersTable(loadingTradePartners.hide());
};

window.showMajors = function() {
    var headers = {
        0: "article",
        1: "color",
        2: "desc",
        3: "enrolled",
        4: "gender",
        5: "icon",
        6: "id",
        7: "keywords",
        8: "name",
        9: "plural_pt",
        10: "url"
    };

    var loadingMajors = dataviva.ui.loading('.classifications-majors .classifications-majors-wrapper');
    loadingMajors.text(dataviva.dictionary['loading'] + "...");

    var MajorsTable = function () {
        this.tableId = '#majors-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-majors-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-majors'
                }
            ],
            "ajax": {
                "url": "/attrs/course_hedu/?depth=2",
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {data: "id"},
                {
                    render: function (data, type, row, meta){
                    return dataviva.course_hedu[row.id].name.truncate(65);
                    }
                },
                {
                    render: function (data, type, row, meta){
                        return dataviva.format.number(row.enrolled, {"key": headers[3]});
                    },
                    className: "table-number",
                    type: 'num-dataviva'
                },
                {data: "color"}
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": true,
            "scroller": true,
            initComplete: function () {
                loadingMajors.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var course_hedu_2 = dataviva.dictionary['course_hedu_2'],
                    course_hedu_6 = dataviva.dictionary['course_hedu_6'];

                buttons.append($("<button>"+course_hedu_2+"</button>").attr("id", 'major-fields').addClass("btn btn-white"));
                buttons.append($("<button>"+course_hedu_6+"</button>").attr("id", 'major-majors').addClass("btn btn-white"));

                $('.classifications-majors-content .classifications-majors-control').append(buttons);

                $('#major-table_filter input').removeClass('input-sm');
                $('#major-table_filter').addClass('pull-right');
                $('#major-fields').addClass('active');

                $('#major-fields').click(function() {
                    loadingMajors.show();
                    majors.table.ajax.url("/attrs/course_hedu/?depth=2").load(loadingMajors.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#major-majors').click(function() {
                    loadingMajors.show();
                    majors.table.ajax.url("/attrs/course_hedu/?depth=6").load(loadingMajors.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-majors .classifications-majors-wrapper .classifications-majors-content').show();
                loadingMajors.hide();
            }
        });
    };
    window.majors = new MajorsTable(loadingMajors.hide());
};

window.showUniversities = function() {
    var headers = {
        0: "article",
        1: "color",
        2: "desc",
        3: "enrolled",
        4: "gender",
        4: "icon",
        5: "id",
        6: "keywords",
        7: "name",
        8: "plural_pt",
        9: "school_type",
        10: "school_type_id",
        11: "url"
    }

    var loadingUniversities = dataviva.ui.loading('.classifications-universities .classifications-universities-wrapper');
    loadingUniversities.text(dataviva.dictionary['loading'] + "...");

    var universitiesTable = function () {
        this.tableId = '#universities-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-universities-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-universities'
                }
            ],
            "ajax": {
                "url": "/attrs/university/?depth=5",
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {"data": "id"},
                {
                    render: function (data, type, row, meta){
                        return dataviva.university[row.id].name.truncate(65);
                    }
                },
                {
                    render: function (data, type, row, meta){
                        return dataviva.format.number(row.enrolled, {"key": headers[3]});
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
                loadingUniversities.show();
                $('#universities-table_filter input').removeClass('input-sm');
                $('#universities-table_filter').addClass('pull-right');
                $('.classifications-universities .classifications-universities-wrapper .classifications-universities-content').show();
                loadingUniversities.hide();
            }
        });
    };
    window.universities = new universitiesTable();
};

window.showBasicCourses = function() {
    var headers = {
        0: "article_pt",
        1: "color",
        2: "desc",
        3: "enrolled",
        4: "gender",
        5: "icon",
        6: "id",
        7: "img_author",
        8: "img_link",
        9: "keywords",
        10: "name",
        11: "plural_pt",
        12: "url",
    }

    var loadingBasicCourses = dataviva.ui.loading('.classifications-basic-courses .classifications-basic-courses-wrapper');
    loadingBasicCourses.text(dataviva.dictionary['loading'] + "...");

    var BasicCoursesTable = function () {
        this.tableId = '#basic-courses-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-basic-courses-control">Bfrtip',
             "buttons": [ 
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-basic-courses'
                }
            ],
            "ajax": {
                "url": "/attrs/course_sc/?depth=2",
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
            {"data": "id"},
            {
                    render: function (data, type, row, meta){
                        return dataviva.course_sc[row.id].name;
                    }
                },
                {
                    render: function (data, type, row, meta){
                        return dataviva.format.number(row.enrolled, {"key": headers[3]});
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
                loadingBasicCourses.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var course_sc_2 = dataviva.dictionary['course_sc_2'],
                    course_sc_5 = dataviva.dictionary['course_sc_5'];

                buttons.append($("<button>"+course_sc_2+"</button>").attr("id", 'basic-courses-fields').addClass("btn btn-white"));
                buttons.append($("<button>"+course_sc_5+"</button>").attr("id", 'basic-courses-courses').addClass("btn btn-white"));

                $('.classifications-basic-courses-content .classifications-basic-courses-control').append(buttons);

                $('#basic-courses-table_filter input').removeClass('input-sm');
                $('#basic-courses-table_filter').addClass('pull-right');
                $('#basic-courses-fields').addClass('active');

                $('#basic-courses-fields').click(function() {
                    loadingBasicCourses.show();
                    basicCourses.table.ajax.url("/attrs/course_sc/?depth=2").load(loadingBasicCourses.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#basic-courses-courses').click(function() {
                    loadingBasicCourses.show();
                    basicCourses.table.ajax.url("/attrs/course_sc/?depth=5").load(loadingBasicCourses.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-basic-courses .classifications-basic-courses-wrapper .classifications-basic-courses-content').show();
                loadingBasicCourses.hide();
            }
        });
    };
    window.basicCourses = new BasicCoursesTable();
};

window.showDemographicInformations = function() {
    // @todo: move translate to babel
    dataviva.dictionary['health_region'] = lang == 'en' ? 'Health Region' : 'Região de Saúde';
    dataviva.dictionary['literacy'] = lang == 'en' ? 'Literacy' : 'Escolaridade';
    dataviva.dictionary['gender'] = lang == 'en' ? 'Gender' : 'Gênero';
    dataviva.dictionary['ethnicity'] = lang == 'en' ? 'Ethnicity' : 'Etnia';

    var loadingDemographicInformations = dataviva.ui.loading('.classifications-demographic-informations .classifications-demographic-informations-wrapper');
    loadingDemographicInformations.text(dataviva.dictionary['loading'] + "...");

    var DemographicInformationsTable = function () {
        this.tableId = '#demographic-informations-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-demographic-informations-control">Bfrtip',
             "buttons": [
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-demographic-informations'
                }
            ],
            "ajax": {
                "url": "/attrs/demographic_information/literacy?lang=" + lang,
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    data: "id"
                },
                {
                    data: "name"
                },
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": true,
            "scroller": true,
            initComplete: function () {
                loadingDemographicInformations.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var literacy = dataviva.dictionary['literacy'];
                    ethnicity = dataviva.dictionary['ethnicity'],
                    gender = dataviva.dictionary['gender'];

                buttons.append($("<button>" + literacy + "</button>").attr("id", 'demographic-informations-literacy').addClass("btn btn-white"));
                buttons.append($("<button>" + ethnicity + "</button>").attr("id", 'demographic-informations-ethnicity').addClass("btn btn-white"));
                buttons.append($("<button>" + gender + "</button>").attr("id", 'demographic-informations-gender').addClass("btn btn-white"));

                $('.classifications-demographic-informations-content .classifications-demographic-informations-control').append(buttons);

                $('#demographic-informations-table_filter input').removeClass('input-sm');
                $('#demographic-informations-table_filter').addClass('pull-right');
                $('#demographic-informations-literacy').addClass('active');

                $('#demographic-informations-literacy').click(function() {
                    loadingDemographicInformations.show();
                    DemographicInformations.table.ajax.url("/attrs/demographic_information/literacy?lang=" + lang).load(loadingDemographicInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#demographic-informations-ethnicity').click(function() {
                    loadingDemographicInformations.show();
                    DemographicInformations.table.ajax.url("/attrs/demographic_information/ethnicity?lang=" + lang).load(loadingDemographicInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#demographic-informations-gender').click(function() {
                    loadingDemographicInformations.show();
                    DemographicInformations.table.ajax.url("/attrs/demographic_information/gender?lang=" + lang).load(loadingDemographicInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-demographic-informations .classifications-demographic-informations-wrapper .classifications-demographic-informations-content').show();
                loadingDemographicInformations.hide();
            }
        });
    };
    window.DemographicInformations = new DemographicInformationsTable();
};

window.showEstablishmentInformations = function() {
    // @todo: move translate to babel
    dataviva.dictionary['legal_nature'] = lang == 'en' ? 'Legal Nature' : 'Natureza Jurídica';
    dataviva.dictionary['simple'] = lang == 'en' ? 'Simples' : 'Simples';
    dataviva.dictionary['establishment_size'] = lang == 'en' ? 'Establishment Size' : 'Tamanho do Estabelecimento';

    var loadingEstablishmentInformations = dataviva.ui.loading('.classifications-demographic-informations .classifications-demographic-informations-wrapper');
    loadingEstablishmentInformations.text(dataviva.dictionary['loading'] + "...");

    var EstablishmentInformationsTable = function () {
        this.tableId = '#establishment-informations-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-establishment-informations-control">Bfrtip',
             "buttons": [
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-establishment-informations'
                }
            ],
            "ajax": {
                "url": "/attrs/establishment_information/legal_nature?lang=" + lang,
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    data: "id"
                },
                {
                    data: "name"
                },
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": true,
            "scroller": true,
            initComplete: function () {
                loadingEstablishmentInformations.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var legal_nature = dataviva.dictionary['legal_nature'];
                    simple = dataviva.dictionary['simple'],
                    establishment_size = dataviva.dictionary['establishment_size'];

                buttons.append($("<button>" + legal_nature + "</button>").attr("id", 'establishment-informations-legal_nature').addClass("btn btn-white"));
                buttons.append($("<button>" + simple + "</button>").attr("id", 'establishment-informations-simple').addClass("btn btn-white"));
                buttons.append($("<button>" + establishment_size + "</button>").attr("id", 'establishment-informations-establishment_size').addClass("btn btn-white"));

                $('.classifications-establishment-informations-content .classifications-establishment-informations-control').append(buttons);

                $('#establishment-informations-table_filter input').removeClass('input-sm');
                $('#establishment-informations-table_filter').addClass('pull-right');
                $('#establishment-informations-legal_nature').addClass('active');

                $('#establishment-informations-legal_nature').click(function() {
                    loadingEstablishmentInformations.show();
                    EstablishmentInformations.table.ajax.url("/attrs/establishment_information/legal_nature?lang=" + lang).load(loadingEstablishmentInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#establishment-informations-simple').click(function() {
                    loadingEstablishmentInformations.show();
                    EstablishmentInformations.table.ajax.url("/attrs/establishment_information/simple?lang=" + lang).load(loadingEstablishmentInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#establishment-informations-establishment_size').click(function() {
                    loadingEstablishmentInformations.show();
                    EstablishmentInformations.table.ajax.url("/attrs/establishment_information/establishment_size?lang=" + lang).load(loadingEstablishmentInformations.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-establishment-informations .classifications-establishment-informations-wrapper .classifications-establishment-informations-content').show();
                loadingEstablishmentInformations.hide();
            }
        });
    };
    window.EstablishmentInformations = new EstablishmentInformationsTable();
};

window.showDatasus = function() {
    // @todo: move translate to babel
    dataviva.dictionary['equipment_type'] = lang == 'en' ? 'Equipment Type' : 'Tipo de Equipamento';
    dataviva.dictionary['equipment_code'] = lang == 'en' ? 'Equipments' : 'Equipamentos';
    dataviva.dictionary['hierarchy_level'] = lang == 'en' ? 'Hierarchy Level' : 'Nível de Hierarquia';
    dataviva.dictionary['bed_type'] = lang == 'en' ? 'Bed Type' : 'Tipo de Leito';
    dataviva.dictionary['unit_type'] = lang == 'en' ? 'Unit Type' : 'Tipo de Unidade';

    var loadingDatasus = dataviva.ui.loading('.classifications-datasus .classifications-datasus-wrapper');
    loadingDatasus.text(dataviva.dictionary['loading'] + "...");

    var DatasusTable = function () {
        this.tableId = '#datasus-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-datasus-control">Bfrtip',
             "buttons": [
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-datasus'
                }
            ],
            "ajax": {
                "url": "/attrs/datasus/equipment_type?lang=" + lang,
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    data: "id"
                },
                {
                    data: "name"
                },
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": true,
            "scroller": true,
            initComplete: function () {
                loadingDatasus.show();
                var buttons = $("<div></div>").addClass("btn-group");

                var equipment_type = dataviva.dictionary['equipment_type'],
                    equipment_code = dataviva.dictionary['equipment_code'],
                    hierarchy_level = dataviva.dictionary['hierarchy_level'],
                    bed_type = dataviva.dictionary['bed_type'],
                    unit_type = dataviva.dictionary['unit_type'];

                buttons.append($("<button>" + equipment_type + "</button>").attr("id", 'datasus-equipment_type').addClass("btn btn-white"));
                buttons.append($("<button>" + equipment_code + "</button>").attr("id", 'datasus-equipment_code').addClass("btn btn-white"));
                buttons.append($("<button>" + hierarchy_level + "</button>").attr("id", 'datasus-hierarchy_level').addClass("btn btn-white"));
                buttons.append($("<button>" + bed_type + "</button>").attr("id", 'datasus-bed_type').addClass("btn btn-white"));
                buttons.append($("<button>" + unit_type + "</button>").attr("id", 'datasus-unit_type').addClass("btn btn-white"));

                $('.classifications-datasus-content .classifications-datasus-control').append(buttons);

                $('#datasus-table_filter input').removeClass('input-sm');
                $('#datasus-table_filter').addClass('pull-right');
                $('#datasus-equipment_type').addClass('active');

                $('#datasus-equipment_type').click(function() {
                    loadingDatasus.show();
                    Datasus.table.ajax.url("/attrs/datasus/equipment_type?lang=" + lang).load(loadingDatasus.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#datasus-equipment_code').click(function() {
                    loadingDatasus.show();
                    Datasus.table.ajax.url("/attrs/datasus/equipment_code?lang=" + lang).load(loadingDatasus.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#datasus-hierarchy_level').click(function() {
                    loadingDatasus.show();
                    Datasus.table.ajax.url("/attrs/datasus/hierarchy_level?lang=" + lang).load(loadingDatasus.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#datasus-bed_type').click(function() {
                    loadingDatasus.show();
                    Datasus.table.ajax.url("/attrs/datasus/bed_type?lang=" + lang).load(loadingDatasus.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('#datasus-unit_type').click(function() {
                    loadingDatasus.show();
                    Datasus.table.ajax.url("/attrs/datasus/unit_type?lang=" + lang).load(loadingDatasus.hide);
                    $(this).addClass('active').siblings().removeClass('active');
                });

                $('.classifications-datasus .classifications-datasus-wrapper .classifications-datasus-content').show();
                loadingDatasus.hide();
            }
        });
    };
    window.Datasus = new DatasusTable();
};

window.showPort = function() {
    // @todo: move translate to babel
    dataviva.dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';

    var loadingPort = dataviva.ui.loading('.classifications-ports .classifications-ports-wrapper');
    loadingPort.text(dataviva.dictionary['loading'] + "...");

    var PortTable = function () {
        this.tableId = '#ports-table';

        this.table = $(this.tableId).DataTable({
            "dom": '<"classifications-ports-control">Bfrtip',
             "buttons": [
                {
                    extend: 'csvHtml5',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    filename: 'dataviva-help-ports'
                }
            ],
            "ajax": {
                "url": "/attrs/port/?lang=" + lang,
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    data: "id"
                },
                {
                    data: "name"
                },
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": true,
            "scroller": true,
            initComplete: function () {
                $('#ports-table_filter input').removeClass('input-sm');
                $('#ports-table_filter').addClass('pull-right');
                $('.classifications-ports .classifications-ports-wrapper .classifications-ports-content').show();
                loadingPort.hide();
            }
        });
    };
    window.Port = new PortTable();
};

$('.help-classifications-locations').on('click', function(){
    dataviva.requireAttrs(['bra'], function() {
        if(!window.locations){ 
            showLocations();
        }
    });
});

$('.help-classifications-industries').on('click', function(){
    dataviva.requireAttrs(['cnae'], function() {
        if(!window.industries){
            showIndustries();
        }
    });
});

$('.help-classifications-occupations').on('click', function(){
    dataviva.requireAttrs(['cbo'], function() {
        if(!window.occupations){
            showOccupations();
        }
    });
});

$('.help-classifications-products').on('click', function(){
    dataviva.requireAttrs(['hs'], function() {
        if(!window.products){
            showProducts();
        }
    });
});

$('.help-classifications-trade-partners').on('click', function(){
    dataviva.requireAttrs(['wld'], function() {
        if(!window.tradePartners){
            showTradePartners();
        }
    });
});

$('.help-classifications-majors').on('click', function(){
    dataviva.requireAttrs(['course_hedu'], function() {
        if(!window.majors){
            showMajors();
        }
    });
});

$('.help-classifications-universities').on('click', function(){
    dataviva.requireAttrs(['university'], function() {
        if(!window.universities){
            showUniversities();
        }
    });
});

$('.help-classifications-basic-courses').on('click', function(){
    dataviva.requireAttrs(['course_sc'], function() {
        if(!window.basicCourses){
            showBasicCourses();
        }
    });
});

$('.help-classifications-demographic-informations').on('click', function(){
    if(!window.DemographicInformations){
        showDemographicInformations();
    }
});

$('.help-classifications-establishment-informations').on('click', function(){
    if(!window.EstablishmentInformations){
        showEstablishmentInformations();
    }
});

$('.help-classifications-datasus').on('click', function(){
    if(!window.Datasus){
        showDatasus();
    }
});

$('.help-classifications-ports').on('click', function(){
    if(!window.Port){
        showPort();
    }
});