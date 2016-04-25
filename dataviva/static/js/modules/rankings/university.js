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
    11: "university_id"
}

var universityTable = function () {
    this.tableId = '#university-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/hedu/all/all/show/all/?order=enrolled.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 10},
            {data: 11},
            {
                render: function (data, type, row, meta){
                    return dataviva.university[row[11]].name
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
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[8], {"key": headers[8]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[9], {"key": headers[9]});
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

            var select = $("<select></select>").attr("id", 'year-selector').addClass("year-selector form-control");

            var year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));

            $('.rankings-content .rankings-control').append(select);

            universityTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               universityTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#university-table_filter input').removeClass('input-sm');
            $('#university-table_filter').addClass('pull-right');

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            universityTable.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['university'], function() {
        window.universityTable = new universityTable();
    });
});
