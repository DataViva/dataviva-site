var LocationWages = function () {
    this.tableId = '#location-wages-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/rais/all/show.9/all/all/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            null,
            null,
            {data: 3},
            {data: 1},
            {data: 4},
            {data: 5},
            {data: 9},
            {data: 10},
            {data: 7},
            {data: 8},
            {data: 12},
            {data: 13},
            {data: 14},
            {data: 15}
        ],
        "columnDefs": [
            {
                "targets": 1,
                "render": function (data, type, row, meta){
                    if (dataviva.bra[row[11]].id_ibge === false){
                        return '-'
                    }
                    else {
                        return dataviva.bra[row[11]].id_ibge
                    }
                }
            },
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.bra[row[11]].name
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
                locationWages.table.ajax.url("/rais/all/show.1/all/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-states').click(function() {
                locationWages.table.ajax.url("/rais/all/show.3/all/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-mesoregions').click(function() {
                locationWages.table.ajax.url("/rais/all/show.5/all/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-microregions').click(function() {
                locationWages.table.ajax.url("/rais/all/show.7/all/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#location-wages-municipalities').click(function() {
                locationWages.table.ajax.url("/rais/all/show.9/all/all/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            locationWages.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['bra'], function() {
        window.locationWages = new LocationWages();
    });
});
