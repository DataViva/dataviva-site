var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "enrolled",
    4: "gender",
    5: "icon",
    6: "id",
    7: "keywords",
    8: "name",
    9: "plural_pt",
    10: "url"
};

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var MajorsTable = function () {
    this.tableId = '#majors-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "ajax": {
            "url": "/attrs/course_hedu/?depth=2",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {data: "id"},
            {
                render: function (data, type, row, meta){
                return dataviva.course_hedu[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.enrolled, {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {data: "color"}
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var buttons = $("<div></div>").addClass("btn-group");

            var course_hedu_2 = dataviva.dictionary['course_hedu_2'],
                course_hedu_6 = dataviva.dictionary['course_hedu_6'];

            buttons.append($("<button>"+course_hedu_2+"</button>").attr("id", 'major-fields').addClass("btn btn-white"));
            buttons.append($("<button>"+course_hedu_6+"</button>").attr("id", 'major-majors').addClass("btn btn-white"));

            $('.classifications-content .classifications-control').append(buttons);

            $('#major-table_filter input').removeClass('input-sm');
            $('#major-table_filter').addClass('pull-right');
            $('#major-fields').addClass('active');

            $('#major-fields').click(function() {
                loadingRankings.show();
                majors.table.ajax.url("/attrs/course_hedu/?depth=2").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#major-majors').click(function() {
                loadingRankings.show();
                majors.table.ajax.url("/attrs/course_hedu/?depth=6").load(loadingRankings.hide);
                $(this).addClass('active').siblings().removeClass('active');
            });

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['course_hedu'], function() {
    window.majors = new MajorsTable();
});
