var EconomicActivitiesTable = function () {
    this.tableId = '#economic-activities-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/rais/all/all/show.6/all/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            null,
            {data: 2},
            {data: 0},
            {data: 3},
            {data: 4},
            {data: 8},
            {data: 9},
            {data: 6},
            {data: 7},
            {data: 12},
            {data: 13},
            {data: 14},
            {data: 15}
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.cnae[row[11]].name
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
                economicActivities.table.ajax.url("/rais/all/all/show.1/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#economic-activities-divisions').click(function() {
                economicActivities.table.ajax.url("/rais/all/all/show.3/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#economic-activities-classes').click(function() {
                economicActivities.table.ajax.url("/rais/all/all/show.6/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            economicActivities.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['cnae'], function() {
        window.economicActivities = new EconomicActivitiesTable();
    });
});
