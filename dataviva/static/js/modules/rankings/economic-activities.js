var EconomicActivitiesTable = function () {
    this.tableId = '#economic-activities-table';

    this.table = $(this.tableId).DataTable({
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
            var select = $('#year-selector')

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

            $('#year-selector').append(select);
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

$(document).ready(function(){

    $('#economic-activities-sections').click(function() {
        economicActivitiesSections();
    });

    $('#economic-activities-divisions').click(function() {
        economicActivitiesDivisions();
    });

    $('#economic-activities-classes').click(function() {
        economicActivitiesClasses();
    });

});
