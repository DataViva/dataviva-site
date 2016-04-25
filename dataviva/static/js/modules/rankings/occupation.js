var headers = {
    0: "year",
    1: "wage",
    2: "num_emp",
    3: "num_jobs",
    4: "num_est",
    5: "wage_avg",
    6: "age_avg",
    7: "wage_growth",
    8: "wage_growth_5",
    9: "num_emp_growth",
    10: "num_emp_growth_5",
    11: "cbo_id",
    12: "cnae_diversity",
    13: "cnae_diversity_eff",
    14: "bra_diversity",
    15: "bra_diversity_eff",
    16: "hist",
    17: "gini"
}

var OccupationTable = function () {
    this.tableId = '#occupation-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"rankings-control">frtip',
        "sAjaxSource": "/rais/all/all/all/show.4/?order=num_jobs.desc",
        "sAjaxDataProp": "data",
        "order": [],
        "columns": [
            {data: 0},
            {data: 11},
            {
                render: function (data, type, row, meta){
                    return dataviva.cbo[row[11]].name
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[3], {"key": headers[3]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[1], {"key": headers[1]});
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
                    return dataviva.format.number(row[9], {"key": headers[9]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[10], {"key": headers[10]});
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
                    return dataviva.format.number(row[12], {"key": headers[12]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[13], {"key": headers[13]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[14], {"key": headers[14]});
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row[15], {"key": headers[15]});
                }
            },
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

            var cbo_1 = dataviva.dictionary['cbo_1'],
                cbo_4 = dataviva.dictionary['cbo_4'],
                year = dataviva.dictionary['year'];

            select.append($('<option value="">'+year+'</option>'));
            buttons.append($("<button>"+cbo_1+"</button>").attr("id", 'occupation-groups').addClass("btn btn-white"));
            buttons.append($("<button>"+cbo_4+"</button>").attr("id", 'occupation-families').addClass("btn btn-white"));

            $('.rankings-content .rankings-control').append(buttons);
            $('.rankings-content .rankings-control').append(select);

            occupationTable.table
                .column( 0 )
                .cache( 'search' )
                .sort()
                .unique()
                .each( function ( d ) {
                    select.append( $('<option value="'+d+'">'+d+'</option>') );
                } );

            select.on( 'change', function () {
               occupationTable.table
                    .column( 0 )
                    .search( $(this).val() )
                    .draw();
            });

            $('#occupation-table_filter input').removeClass('input-sm');
            $('#occupation-table_filter').addClass('pull-right');
            $('#occupation-families').addClass('active');

            $('#occupation-groups').click(function() {
                occupationTable.table.ajax.url("/rais/all/all/all/show.1/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            $('#occupation-families').click(function() {
                occupationTable.table.ajax.url("/rais/all/all/all/show.4/?order=num_jobs.desc").load();
                $(this).addClass('active').siblings().removeClass('active');
            });

            var lastYear = $('#year-selector option').last().val();
            $('#year-selector').val(lastYear);
            occupationTable.table
                    .column( 0 )
                    .search(lastYear)
                    .draw();
        }
    });
};

$(document).ready(function() {
    dataviva.requireAttrs(['cbo'], function() {
        window.occupationTable = new OccupationTable();
    });
});
