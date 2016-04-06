var EconomicActivitiesTable = function () {
    this.tableId = '#economic-activities-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/rais/all/all/show.1/all/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null,
            { "bVisible": false },
            null,
            { "bVisible": false },
            null,
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            null,
            null,
            null,
            null,
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false },
            { "bVisible": false }
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Seções</button>").attr("id", 'economic-activities-sections').addClass("btn btn-white"));
            buttons.append($("<button>Divisões</button>").attr("id", 'economic-activities-divisions').addClass("btn btn-white"));
            buttons.append($("<button>Classes</button>").attr("id", 'economic-activities-classes').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            economicActivities.table
                .column( 10 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               economicActivities.table
                    .column( 10 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#economic-activities-table_filter input').removeClass('input-sm');
            $('#economic-activities-table_filter').addClass('pull-right');

            $('#economic-activities-sections').click(function() {
                economicActivitiesSections();
            });

            $('#economic-activities-divisions').click(function() {
                economicActivitiesDivisions();
            });

            $('#economic-activities-classes').click(function() {
                economicActivitiesClasses();
            });
        }
    });
};

var economicActivities = new EconomicActivitiesTable();

var economicActivitiesSections = function() {
    economicActivities.table.ajax.url("/rais/all/all/show.1/all/?order=num_jobs.desc").load();
};

var economicActivitiesDivisions = function() {
    economicActivities.table.ajax.url("/rais/all/all/show.3/all/?order=num_jobs.desc").load();
};

var economicActivitiesClasses = function() {
    economicActivities.table.ajax.url("/rais/all/all/show.6/all/?order=num_jobs.desc").load();
};
