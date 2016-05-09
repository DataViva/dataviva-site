var headers = {
    0: "cnae_id",
    1: "hs_id"
}

var loadingRankings = dataviva.ui.loading('.classifications .classifications-wrapper');
loadingRankings.text(dataviva.dictionary['loading'] + "...");

var IndustryProductTable = function () {
    this.tableId = '#crosswalk-ip-table';

    this.table = $(this.tableId).DataTable({
        "ajax": {
            "url": "/help/crosswalk/ip",
            "dataSrc": "data",
            "cache": true,
        },
        "order": [],
        "columns": [
            {
                render: function (data, type, row, meta){
                    if (dataviva.cnae[row[0]]){
                        return dataviva.cnae[row[0]].name + ' (' + row[0] + ')';
                    }
                    else{
                        return '-';
                    }

                }
            },
            {
                render: function (data, type, row, meta){
                    return dataviva.hs[row[1]].name + ' (' + row[1] + ')';
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

dataviva.requireAttrs(['hs', 'cnae'], function() {
    window.industryProduct = new IndustryProductTable(loadingRankings.hide);
});
