var MajorTable = function () {
    this.tableId = '#major-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/all/show.2/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "aoColumns": [
            null, //enrolled
            null, //graduates
            null, //entrants
            { "bVisible": false }, //morning
            { "bVisible": false }, //afternoon
            { "bVisible": false }, //night
            { "bVisible": false }, //full_time
            { "bVisible": false }, //age
            { "bVisible": false }, //graduates_growth
            { "bVisible": false }, //enrolled_growth
            null, //year
            null //course_hedu_id
        ],
        "deferRender": true,
        "scrollY": 500,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {
            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control"),
                buttons = $("<div></div>").addClass("btn-group");

            select.append( $('<option value="">Ano</option>') );
            buttons.append($("<button>Campos</button>").attr("id", 'major-fields').addClass("btn btn-white"));
            buttons.append($("<button>Ensino Superior</button>").attr("id", 'major-majors').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            majorTable.table
                .column( 10 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               majorTable.table
                    .column( 10 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#major-table_filter input').removeClass('input-sm');
            $('#major-table_filter').addClass('pull-right');

            $('#major-fields').click(function() {
                majorFields();
            });

            $('#major-majors').click(function() {
                majorMajors();
            });
        }
    });
};

var majorTable = new MajorTable();

var majorFields = function() {
    majorTable.table.ajax.url("/hedu/all/all/all/show.2/?order=enrolled.desc").load();
};

var majorMajors = function() {
    majorTable.table.ajax.url("/hedu/all/all/all/show.6/?order=enrolled.desc").load();
};
