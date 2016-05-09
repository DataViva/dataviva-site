var headers = {
    0: "cbo_id",
    1: "course_hedu_id"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var OccupationCourseTable = function () {
    this.tableId = '#crosswalk-oc-table';

    this.table = $(this.tableId).DataTable({
        "ajax": {
            "url": "/help/crosswalk/oc",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                        return dataviva.cbo[row[0]].name + ' (' + row[0] + ')';
                }
            },
            {
                render: function (data, type, row, meta){
                    if (dataviva.course_hedu[row[1]]){
                        return dataviva.course_hedu[row[1]].name + ' (' + row[1] + ')';
                    }
                    else{
                        return '-';
                    }
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
            loadingRankings.hide();
            $('.classifications .classifications-wrapper .classifications-content').show();
        }
    });
};

dataviva.requireAttrs(['cbo', 'course_hedu'], function() {
    window.occupationCourse = new OccupationCourseTable(loadingRankings.hide);
});
