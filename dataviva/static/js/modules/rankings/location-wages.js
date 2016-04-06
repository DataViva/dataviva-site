var WagesTable = function () {
    this.tableId = '#wages-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/rais/all/show.1/all/all/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //year
            { "bVisible": false }, //wage
            { "bVisible": false }, //num_emp
            null, //num_jobs
            null, //num_est
            null, //wage_avg
            { "bVisible": false }, //age_avg
            { "bVisible": false }, //wage_growth
            { "bVisible": false }, //wage_growth_5
            { "bVisible": false }, //num_emp_growth
            { "bVisible": false }, //num_emp_growth_5
            null, //bra_id
            null, //cnae_diversity
            null, //cnae_diversity_eff
            { "bVisible": false }, //cbo_diversity
            { "bVisible": false }, //cbo_diversity_eff
            { "bVisible": false }, //hist
            { "bVisible": false } //gini
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $('#year-selector')

            wagesTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               wagesTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
        }
    });
};

var wagesTable = new WagesTable();

var wagesRegions = function() {
    wagesTable.table.ajax.url("/rais/all/show.1/all/all/?order=num_jobs.desc").load();
};

var wagesStates = function() {
    wagesTable.table.ajax.url("/rais/all/show.3/all/all/?order=num_jobs.desc").load();
};

var wagesMesoregions = function() {
    wagesTable.table.ajax.url("/rais/all/show.5/all/all/?order=num_jobs.desc").load();
};

var wagesMicroregions = function() {
    wagesTable.table.ajax.url("/rais/all/show.7/all/all/?order=num_jobs.desc").load();
};

var wagesMunicipalities = function() {
    wagesTable.table.ajax.url("/rais/all/show.9/all/all/?order=num_jobs.desc").load();
};

$(document).ready(function(){

    $('#location-wages-regions').click(function() {
        wagesRegions();
    });

    $('#location-wages-states').click(function() {
        wagesStates();
    });

    $('#location-wages-mesoregions').click(function() {
        wagesMesoregions();
    });

    $('#location-wages-microregions').click(function() {
        wagesMicroRegions();
    });

    $('#location-wages-municipalities').click(function() {
        wagesMunicipalities();
    });

});
