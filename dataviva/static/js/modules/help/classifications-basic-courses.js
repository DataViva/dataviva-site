var headers = {
    0: "article_pt",
    1: "color",
    2: "desc",
    3: "enrolled",
    4: "gender",
    5: "icon",
    6: "id",
    7: "img_author",
    8: "img_link",
    9: "keywords",
    10: "name",
    11: "plural_pt",
    12: "url",
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var BasicCoursesTable = function () {
    this.tableId = '#basic-courses-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/course_sc/?depth=2",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
        {"data": "id"},
        {
                render: function (data, type, row, meta){
                    return dataviva.course_sc[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.enrolled, {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
        {"data": "color"},
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var buttons = $("<div></div>").addClass("btn-group");

            var course_sc_2 = dataviva.dictionary['course_sc_2'],
                course_sc_5 = dataviva.dictionary['course_sc_5'];

            buttons.append($("<button>"+course_sc_2+"</button>").attr("id", 'basic-courses-fields').addClass("btn btn-white"));
            buttons.append($("<button>"+course_sc_5+"</button>").attr("id", 'basic-courses-courses').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#basic-courses-table_filter input').removeClass('input-sm');
            $('#basic-courses-table_filter').addClass('pull-right');
            $('#basic-courses-fields').addClass('active');

            $('#basic-courses-fields').click(function() {
                loadingRankings.show();
                basicCourses.table.ajax.url("/attrs/course_sc/?depth=2").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#basic-courses-courses').click(function() {
                loadingRankings.show();
                basicCourses.table.ajax.url("/attrs/course_sc/?depth=5").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['course_sc'], function() {
    window.basicCourses = new BasicCoursesTable(loadingRankings.hide);
});
    