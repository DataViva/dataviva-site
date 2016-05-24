window.showCrosswalkPI = function() {
    var headers = {
        0: "hs_id",
        1: "cnae_id"
    }

    var loadingCrosswalkPI = dataviva.ui.loading('.crosswalk-pi .crosswalk-pi-wrapper');
    loadingCrosswalkPI.text(dataviva.dictionary['loading'] + "...");

    var ProductIndustryTable = function () {
        this.tableId = '#crosswalk-pi-table';

        this.table = $(this.tableId).DataTable({
            "ajax": {
                "url": "/help/crosswalk/pi",
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    render: function (data, type, row, meta){
                        return dataviva.hs[row[0]].name.truncate(40) + ' (' + row[0] + ')';
                    }
                },
                {
                    render: function (data, type, row, meta){
                        result = '';
                        for(i=0; i<row[1].length; i++){
                            if(dataviva.cnae[ row[1][i] ])
                                result += (i != 0 ? '</br>' : '') + dataviva.cnae[row[1][i]].name.truncate(40) + ' (' + row[1][i] + ')';
                        }
                        return result != '' ? result : "-";
                    }
                }
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": false,
            "scroller": true,
            initComplete: function () {
                loadingCrosswalkPI.show();
                $('.crosswalk-pi .crosswalk-pi-wrapper .crosswalk-pi-content').show();
                loadingCrosswalkPI.hide();
            }
        });
    };
    window.productIndustry = new ProductIndustryTable(loadingCrosswalkPI.hide());
};

window.showCrosswalkIP = function() {
    var headers = {
        0: "cnae_id",
        1: "hs_id"
    }

    var loadingCrosswalkIP = dataviva.ui.loading('.crosswalk-ip .crosswalk-ip-wrapper');
    loadingCrosswalkIP.text(dataviva.dictionary['loading'] + "...");

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
                            return row[0];
                        }

                    }
                },
                {
                    render: function (data, type, row, meta){
                        result = '';
                        for(i=0; i<row[1].length; i++){
                            if(dataviva.hs[ row[1][i] ])
                                result += (i != 0 ? '</br>' : '') + dataviva.hs[row[1][i]].name.truncate(40) + ' (' + row[1][i] + ')';
                        }
                        return result != '' ? result : "-";
                    }
                }
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": false,
            "scroller": true,
            initComplete: function () {
                loadingCrosswalkIP.show();
                $('.crosswalk-ip .crosswalk-ip-wrapper .crosswalk-ip-content').show();
                loadingCrosswalkIP.hide();
            }
        });
    };
    window.IndustryProduct = new IndustryProductTable(loadingCrosswalkIP.hide());
};

window.showCrosswalkOC = function() {
    var headers = {
        0: "cbo_id",
        1: "course_hedu_id"
    }

    var loadingCrosswalkOC = dataviva.ui.loading('.crosswalk-oc .crosswalk-oc-wrapper');
    loadingCrosswalkOC.text(dataviva.dictionary['loading'] + "...");

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
                        result = '';
                        for(i=0; i<row[1].length; i++){
                            if(dataviva.course_hedu[ row[1][i] ])
                                result += (i != 0 ? '</br>' : '') + dataviva.course_hedu[row[1][i]].name.truncate(40) + ' (' + row[1][i] + ')';
                        }
                        return result != '' ? result : "-";
                    }
                }
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": false,
            "scroller": true,
            initComplete: function () {
                loadingCrosswalkOC.show();
                $('.crosswalk-oc .crosswalk-oc-wrapper .crosswalk-oc-content').show();
                loadingCrosswalkOC.hide();
            }
        });
    };
    window.occupationCourse = new OccupationCourseTable(loadingCrosswalkOC.hide());
};

window.showCrosswalkCO = function() {
    var headers = {
        0: "course_hedu_id",
        1: "cbo_id"
    }

    var loadingCrosswalkCO = dataviva.ui.loading('.crosswalk-co .crosswalk-co-wrapper');
    loadingCrosswalkCO.text(dataviva.dictionary['loading'] + "...");

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
                            return row[0];
                        }
                    }
                },
                {
                    render: function (data, type, row, meta){
                        result = '';
                        for(i=0; i<row[1].length; i++){
                            if(dataviva.cbo[ row[1][i] ])
                                result += (i != 0 ? '</br>' : '') + dataviva.cbo[row[1][i]].name.truncate(40) + ' (' + row[1][i] + ')';
                        }
                        return result != '' ? result : "-";
                    }
                },
            ],
            "deferRender": true,
            "language": dataviva.datatables.language,
            "scrollY": 500,
            "scrollX": true,
            "scrollCollapse": false,
            "scroller": true,
            initComplete: function () {
                loadingCrosswalkCO.show();
                $('.crosswalk-co .crosswalk-co-wrapper .crosswalk-co-content').show();
                loadingCrosswalkCO.hide();
            }
        });
    };
    window.courseOccupation = new CourseOccupationTable(loadingCrosswalkCO.hide());
};

$('#question-crosswalk-pi').on('click', function(){
    if(!window.productIndustry){
        showCrosswalkPI()
    }
});

$('#question-crosswalk-ip').on('click', function(){
    if(!window.IndustryProduct){
        showCrosswalkIP()
    }
});

$('#question-crosswalk-oc').on('click', function(){
    if(!window.occupationCourse){
        showCrosswalkOC()
    }
});

$('#question-crosswalk-co').on('click', function(){
    if(!window.courseOccupation){
        showCrosswalkCO();
    }
});
