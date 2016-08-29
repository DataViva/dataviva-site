var headers = {
    0: "wage",
    1: "num_emp",
    2: "num_jobs",
    3: "num_est",
    4: "wage_avg",
    5: "age_avg",
    6: "wage_growth",
    7: "wage_growth_5",
    8: "num_emp_growth",
    9: "num_emp_growth_5",
    10: "year",
    11: "cnae_id",
    12: "cbo_diversity",
    13: "cbo_diversity_eff",
    14: "bra_diversity",
    15: "bra_diversity_eff",
    16: "hist",
    17: "gini"
 }

var loadingRankings = dataviva.ui.loading('.rankings .rankings-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var EconomicActivitiesTable = function () {
    this.tableId = '#economic-activities-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">Bfrtip',
        "buttons": [ 
            {
                extend: 'csvHtml5',
                text: '<i class="fa fa-floppy-o fa-lg"></i>',
                filename: 'rankings-economic-activities'
            }
        ],
        "ajax": {
            "url": "/rais/all/all/show.6/all/?order=num_jobs.desc",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            {
                render: function (data, type, row, meta){
                    return dataviva.cnae[row[11]].name.truncate(35);
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[2], {"key": headers[2]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[0], {"key": headers[0]});
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
                    return dataviva.format.number(row[4], {"key": headers[4]});
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
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[15], {"key": headers[15]});
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

            var cnae_1 = dataviva.dictionary['cnae_1'],
                cnae_3 = dataviva.dictionary['cnae_3'],
                cnae_6 = dataviva.dictionary['cnae_6'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+cnae_1+"</button>").attr("id", 'economic-activities-sections').addClass("btn btn-white"));
            buttons.append($("<button>"+cnae_3+"</button>").attr("id", 'economic-activities-divisions').addClass("btn btn-white"));
            buttons.append($("<button>"+cnae_6+"</button>").attr("id", 'economic-activities-classes').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            economicActivities.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               economicActivities.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#economic-activities-table_filter input').removeClass('input-sm');
            $('#economic-activities-table_filter').addClass('pull-right');
            $('#economic-activities-classes').addClass('active');

            $('#economic-activities-sections').click(function() {
                loadingRankings.show();
                economicActivities.table.ajax.url("/rais/all/all/show.1/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#economic-activities-divisions').click(function() {
                loadingRankings.show();
                economicActivities.table.ajax.url("/rais/all/all/show.3/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#economic-activities-classes').click(function() {
                loadingRankings.show();
                economicActivities.table.ajax.url("/rais/all/all/show.6/all/?order=num_jobs.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            economicActivities.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();

            loadingRankings.hide();
            $('.rankings .rankings-wrapper .rankings-content').show();
        }
    });
};

dataviva.requireAttrs(['cnae'], function() {
    window.economicActivities = new EconomicActivitiesTable();
});
