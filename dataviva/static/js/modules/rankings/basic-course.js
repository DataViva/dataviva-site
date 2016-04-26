var headers = {
    0: "year",
    1: "age",
    2: "classes",
    3: "enrolled",
    4: "enrolled_growth",
    5: "enrolled_growth_5",
    6: "course_sc_id"
}

var loadingRankings = dataviva.ui.loading('.rankings .rankings-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var BasicCourseTable = function () {
    this.tableId = '#basic-course-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "ajax": {
            "url": "/sc/all/all/all/show.5/?order=enrolled.desc",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {data: 0},
            {data: 6},
            {
                render: function (data, type, row, meta){
                    return dataviva.course_sc[row[6]].name.truncate(35);
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[2], {"key": headers[2]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[1], {"key": headers[1]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[4], {"key": headers[4]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[5], {"key": headers[5]});
                },
                className: "table-number",
                type: 'num-dataviva'
            }
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
            $('#basic-course-courses').addClass('active');

            $('#basic-course-fields').click(function() {
                loadingRankings.show();
                basicCourseTable.table.ajax.url("/sc/all/all/all/show.2/?order=enrolled.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#basic-course-courses').click(function() {
                loadingRankings.show();
                basicCourseTable.table.ajax.url("/sc/all/all/all/show.5/?order=enrolled.desc").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            basicCourseTable.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();

            loadingRankings.hide();
            $('.rankings .rankings-wrapper .rankings-content').show();
        }
    });
};

dataviva.requireAttrs(['course_sc'], function() {
    window.basicCourseTable = new BasicCourseTable();
});
    