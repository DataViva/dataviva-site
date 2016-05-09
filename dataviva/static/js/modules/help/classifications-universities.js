var headers = {
    0: "article",
    1: "color",
    2: "desc",
    3: "enrolled",
    4: "gender",
    4: "icon",
    5: "id",
    6: "keywords",
    7: "name",
    8: "plural_pt",
    9: "school_type",
    10: "school_type_id",
    11: "url"
}


var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var universitiesTable = function () {
    this.tableId = '#universities-table';

    this.table = $(this.tableId).DataTable({
        "dom": '<"classifications-control">frtip',
        "ajax": {
            "url": "/attrs/university/?depth=5",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {"data": "id"},
            {
                render: function (data, type, row, meta){
                    return dataviva.university[row.id].name;
                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.format.number(row.enrolled, {"key": headers[3]});
                },
                className: "table-number",
                type: 'num-dataviva'
            },
            {"data": "color"}
        ],
        "deferRender": true,
        "language": dataviva.datatables.language,
        "scrollY": 500,
        "scrollX": true,
        "scrollCollapse": true,
        "scroller": true,
        initComplete: function () {

            $('#universities-table_filter input').removeClass('input-sm');
            $('#universities-table_filter').addClass('pull-right');

            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

    dataviva.requireAttrs(['university'], function() {
        window.universities = new universitiesTable();
    });
