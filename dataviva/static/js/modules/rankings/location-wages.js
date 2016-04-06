var WagesTable = function () {
    this.tableId = '#location-wages-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
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
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Regiões</button>").attr("id", 'location-wages-regions').addClass("btn btn-white"));
            buttons.append($("<button>Estados</button>").attr("id", 'location-wages-states').addClass("btn btn-white"));
            buttons.append($("<button>Mesoregiões</button>").attr("id", 'location-wages-mesoregions').addClass("btn btn-white"));
            buttons.append($("<button>Microregiões</button>").attr("id", 'location-wages-microregions').addClass("btn btn-white"));
            buttons.append($("<button>Municípios</button>").attr("id", 'location-wages-municipalities').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

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

            $('#location-wages-table_filter input').removeClass('input-sm');
            $('#location-wages-table_filter').addClass('pull-right');

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
                wagesMicroregions();
            });

            $('#location-wages-municipalities').click(function() {
                wagesMunicipalities();
            });
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
