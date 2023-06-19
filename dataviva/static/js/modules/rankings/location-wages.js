var headers = {
    0: "id_ibge",
    1: "location",
    2: "year",
    3: "wage",
    4: "num_jobs",
    5: "wage_avg",
    6: "wage_growth",
    7: "wage_growth_5",
    8: "num_emp_growth",
    9: "num_emp_growth_5",
    11: "cnae_diversity",
    12: "cnae_diversity_eff",
    13: "cbo_diversity",
    14: "cbo_diversity_eff",
}

var loadingRankings = dataviva.ui.loading('.rankings .rankings-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var LocationWages = function () {
    this.tableId = '#location-wages-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">Bfrtip',
        "buttons": [ 
            {
                extend: 'csvHtml5',
                text: '<i class="fa fa-floppy-o fa-lg"></i>',
                filename: 'rankings-location-wages-and-employment'
            }
        ],
        "ajax": {
            "url": "/rais/all/show.9/all/all/?order=num_jobs.desc",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {data: 2},
            {
                render: function (data, type, row, meta){

                    return row[0] === null ? '-' : row[0];
                }
            },
            {
                render: function (data, type, row, meta){
                    var abbreviation = dataviva.bra[row[10]].abbreviation;
                    return row[1].truncate(35) + (abbreviation ? " - " + abbreviation : "");
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[4], {"key": headers[4]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[5], {"key": headers[5]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[8], {"key": headers[8]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[9], {"key": headers[9]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[6], {"key": headers[6]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[7], {"key": headers[7]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[11], {"key": headers[11]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[12], {"key": headers[12]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[13], {"key": headers[13]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[14], {"key": headers[14]});
                },
                className: "table-number",
                type: 'num-dataviva'
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

            var bra_1 = dataviva.dictionary['bra_1'],
                bra_3 = dataviva.dictionary['bra_3'],
                bra_5 = dataviva.dictionary['bra_5'],
                bra_7 = dataviva.dictionary['bra_7'],
                bra_9 = dataviva.dictionary['bra_9'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+bra_1+"</button>").attr("id", 'location-wages-regions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_3+"</button>").attr("id", 'location-wages-states').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_5+"</button>").attr("id", 'location-wages-mesoregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_7+"</button>").attr("id", 'location-wages-microregions').addClass("btn btn-white"));
            buttons.append($("<button>"+bra_9+"</button>").attr("id", 'location-wages-municipalities').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            locationWages.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               locationWages.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#location-wages-table_filter input').removeClass('input-sm');
            $('#location-wages-table_filter').addClass('pull-right');
            $('#location-wages-municipalities').addClass('active');

            $('#location-wages-regions').click(function() {
                loadingRankings.show();
                locationWages.table.ajax.url("/rais/all/show.1/all/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-states').click(function() {
                loadingRankings.show();
                locationWages.table.ajax.url("/rais/all/show.3/all/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-mesoregions').click(function() {
                loadingRankings.show();
                locationWages.table.ajax.url("/rais/all/show.5/all/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-microregions').click(function() {
                loadingRankings.show();
                locationWages.table.ajax.url("/rais/all/show.7/all/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-municipalities').click(function() {
                loadingRankings.show();
                locationWages.table.ajax.url("/rais/all/show.9/all/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            locationWages.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();

            loadingRankings.hide();
            $('.rankings .rankings-wrapper .rankings-content').show();
        }
    });
};

dataviva.requireAttrs(['bra'], function() {
    window.locationWages = new LocationWages();
});
