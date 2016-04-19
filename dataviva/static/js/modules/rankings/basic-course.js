var BasicCourseTable = function () {
    this.tableId = '#basic-course-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/sc/all/all/all/show.2/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            {data: 6},
            null,
            {data: 3},
            {data: 2},
            {data: 1},
        ],
        "columnDefs": [
            {
                "targets": 2,
                "render": function (data, type, row, meta){
                    return dataviva.course_sc[row[6]].name
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

            var course_sc_2 = dataviva.dictionary['course_sc_2'],
                course_sc_5 = dataviva.dictionary['course_sc_5'],
                year = dataviva.dictionary['year'];

            select.append( $('<option value="">'+year+'</option>') );
            buttons.append($("<button>"+course_sc_2+"</button>").attr("id", 'basic-course-fields').addClass("btn btn-white"));
            buttons.append($("<button>"+course_sc_5+"</button>").attr("id", 'basic-course-courses').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            basicCourseTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               basicCourseTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#basic-course-table_filter input').removeClass('input-sm');
            $('#basic-course-table_filter').addClass('pull-right');

            $('#basic-course-fields').click(function() {
                basicCourseTable.table.ajax.url("/sc/all/all/all/show.2/?order=enrolled.desc").load();
            });

            $('#basic-course-courses').click(function() {
                basicCourseTable.table.ajax.url("/sc/all/all/all/show.5/?order=enrolled.desc").load();
            });
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['course_sc'], function() {
        window.basicCourseTable = new BasicCourseTable();
    });
});