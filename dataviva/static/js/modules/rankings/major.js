var MajorTable = function () {
    this.tableId = '#major-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/all/show.2/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            null,
            {data: 0},
            {data: 1},
            {data: 2},
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.course_hedu[row[11]].name
                }
            },
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            var course_hedu_2 = dataviva.dictionary['course_hedu_2'],
                course_hedu_6 = dataviva.dictionary['course_hedu_6'],
                year = dataviva.dictionary['year'];

            select.append( $('<option value="">'+year+'</option>') );
            buttons.append($("<button>"+course_hedu_2+"</button>").attr("id", 'major-fields').addClass("btn btn-white"));
            buttons.append($("<button>"+course_hedu_6+"</button>").attr("id", 'major-majors').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            majorTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               majorTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#major-table_filter input').removeClass('input-sm');
            $('#major-table_filter').addClass('pull-right');

            $('#major-fields').click(function() {
                majorTable.table.ajax.url("/hedu/all/all/all/show.2/?order=enrolled.desc").load();
            });

            $('#major-majors').click(function() {
                majorTable.table.ajax.url("/hedu/all/all/all/show.6/?order=enrolled.desc").load();
            });
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['course_hedu'], function() {
        window.majorTable = new MajorTable();
    });
});
