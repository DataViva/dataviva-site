var BasicCourseTable = function () {
    this.tableId = '#basic-course-table';

    this.table = $(this.tableId).DataTable({
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
            var select = $('#year-selector')

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

            $('#year-selector').append(select);
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

$(document).ready(function(){

    $('#basic-course-fields').click(function() {
        basicCourseFields();
    });

    $('#basic-course-courses').click(function() {
        basicCourseCourses();
    });

});
