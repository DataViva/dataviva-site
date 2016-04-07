var BasicCourseTable = function () {
    this.tableId = '#basic-course-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/sc/all/all/all/show.2/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //year
            null, //age
            null, //classes
            null, //enrolled
            { "bVisible": false }, //enrolled_growth
            { "bVisible": false }, //enrolled_growth_5
            null //course_sc_id
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Campos</button>").attr("id", 'basic-course-fields').addClass("btn btn-white"));
            buttons.append($("<button>Cursos</button>").attr("id", 'basic-course-courses').addClass("btn btn-white"));

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
                basicCourseFields();
            });

            $('#basic-course-courses').click(function() {
                basicCourseCourses();
            });
        }
    });
};

var basicCourseTable = new BasicCourseTable();

var basicCourseFields = function() {
    basicCourseTable.table.ajax.url("/sc/all/all/all/show.2/?order=enrolled.desc").load();
};

var basicCourseCourses = function() {
    basicCourseTable.table.ajax.url("/sc/all/all/all/show.5/?order=enrolled.desc").load();
};
