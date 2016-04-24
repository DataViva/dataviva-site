var OccupationTable = function () {
    this.tableId = '#occupation-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/rais/all/all/all/show.4/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            {data: 11},
            null,
            {data: 3},
            {data: 1},
            {data: 4},
            {data: 5},
            {data: 6},
            {data: 9},
            {data: 10},
            {data: 7},
            {data: 8},
            {data: 12},
            {data: 13},
            {data: 14},
            {data: 15},
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.cbo[row[11]].name
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

            var cbo_1 = dataviva.dictionary['cbo_1'],
                cbo_4 = dataviva.dictionary['cbo_4'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+cbo_1+"</button>").attr("id", 'occupation-groups').addClass("btn btn-white"));
            buttons.append($("<button>"+cbo_4+"</button>").attr("id", 'occupation-families').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

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

            $('#occupation-table_filter input').removeClass('input-sm');
            $('#occupation-table_filter').addClass('pull-right');
            $('#occupation-families').addClass('active');

            $('#occupation-groups').click(function() {
                occupationTable.table.ajax.url("/rais/all/all/all/show.1/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#occupation-families').click(function() {
                occupationTable.table.ajax.url("/rais/all/all/all/show.4/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            occupationTable.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['cbo'], function() {
        window.occupationTable = new OccupationTable();
    });
});
