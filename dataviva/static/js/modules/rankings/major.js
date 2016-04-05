var MajorTable = function () {
    this.tableId = '#major-table';

    this.table = $(this.tableId).DataTable({
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
            var select = $('#year-selector')

            majorTable.table
                .column( 11 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               majorTable.table
                    .column( 11 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#year-selector').append(select);
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

$(document).ready(function(){

    $('#major-fields').click(function() {
        majorFields();
    });

    $('#major-majors').click(function() {
        majorMajors();
    });

});
