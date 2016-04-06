var OccupationTable = function () {
    this.tableId = '#occupation-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/rais/all/all/all/show.1/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //year a
            null, //wage a
           { "bVisible": false }, //num_emp
            null, //num_jobs a
            { "bVisible": false }, //num_est
            null, //wage_avg a
            { "bVisible": false }, //age_avg
            { "bVisible": false }, //wage_growth
            { "bVisible": false }, //wage_growth_5
            { "bVisible": false }, //num_emp_growth
            { "bVisible": false }, //num_emp_growth_5
            null, //cbo_id
            null, //cnae_diversity a
            null, //cnae_diversity_eff a
            { "bVisible": false }, //bra_diversity
            { "bVisible": false }, //bra_diversity_eff
            { "bVisible": false }, //hist
            { "bVisible": false } //gini
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $('#year-selector')

            occupationTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               occupationTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var occupationTable = new OccupationTable();

var occupationGroups = function() {
    occupationTable.table.ajax.url("/rais/all/all/all/show.1/?order=num_jobs.desc").load();
};

var occupationFamilies = function() {
    occupationTable.table.ajax.url("/rais/all/all/all/show.4/?order=num_jobs.desc").load();
};


$(document).ready(function(){

    $('#occupation-groups').click(function() {
        occupationGroups();
    });

    $('#occupation-families').click(function() {
        occupationFamilies();
    });

});
