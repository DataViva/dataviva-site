var headers = {
    0: "course_hedu_id",
    1: "cbo_id"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var CourseOccupationTable = function () {
    this.tableId = '#crosswalk-co-table';

    this.table = $(this.tableId).DataTable({
        "ajax": {
            "url": "/help/crosswalk/co",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                    if (dataviva.course_hedu[row[0]]){
                        return dataviva.course_hedu[row[0]].name + ' (' + row[0] + ')';
                    }
                    else{
                        return '-';
                    }
                }
            },
            {
                render: function (data, type, row, meta){
                        return dataviva.cbo[row[1]].name + ' (' + row[1] + ')';
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
            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['cbo', 'course_hedu'], function() {
    window.courseOccupation = new CourseOccupationTable(loadingRankings.hide);
});
