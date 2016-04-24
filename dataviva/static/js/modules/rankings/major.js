var headers = {
    0: "enrolled",
    1: "graduates",
    2: "entrants",
    3: "morning",
    4: "afternoon",
    5: "night",
    6: "full_time",
    7: "age",
    8: "graduates_growth",
    9: "enrolled_growth",
    10: "year",
    11: "course_hedu_id"
};

var MajorTable = function () {
    this.tableId = '#major-table';
//dataviva.format.number(d.wage_avg, {"key": "wage_avg"})
    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/all/show.6/?order=enrolled.desc",
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            {
                render: function (data, type, row, meta){
                    return dataviva.course_hedu[row[11]].name.toTitleCase().truncate(35);
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[0], {"key": headers[0]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[1], {"key": headers[1]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[2], {"key": headers[2]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[4], {"key": headers[4]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[5], {"key": headers[5]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[6], {"key": headers[6]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[7], {"key": headers[7]});
                }
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
            $('#major-majors').addClass('active');

            $('#major-fields').click(function() {
                majorTable.table.ajax.url("/hedu/all/all/all/show.2/?order=enrolled.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#major-majors').click(function() {
                majorTable.table.ajax.url("/hedu/all/all/all/show.6/?order=enrolled.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            majorTable.table
                    .column(0)
                    .search(lastYear)
                    .draw();
        }
    });
};

dataviva.requireAttrs(['course_hedu'], function() {
    window.majorTable = new MajorTable();
});
