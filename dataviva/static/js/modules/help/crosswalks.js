//attr1 and attr2 refers to crosswalk_table, download(pi, hs, cnae)   
function download(crosswalk_table, attr1, attr2){
    $.ajax({
        dataType: 'json',
        method: 'GET',
        url: "/help/crosswalk/" + crosswalk_table + "?download=true",
        success: function (response) {
            
            var attr1_name = (attr1 != 'course_sc') ? dataviva.dictionary[attr1] : dataviva.dictionary['course_sc'].split(' ')[1],
                attr2_name = (attr2 != 'course_sc') ? dataviva.dictionary[attr2] : dataviva.dictionary['course_sc'].split(' ')[1];

            var csv = attr1_name + " ID," + attr1_name + " Name," +
                    attr2_name + " ID,"+  attr2_name + " Name\n";

            response.data.forEach(function(row){

                if(row[0] && row[1]){

                    if(attr1.search('course') == 0){
                        attr1 = (row[0].match(/^[0-9]+$/)) ? 'course_sc' : 'course_hedu'
                    }

                    if(attr2.search('course') == 0){
                        attr2 = (row[1].match(/^[0-9]+$/)) ? 'course_sc' : 'course_hedu'
                    }

                    if(dataviva[attr1][row[0]] && dataviva[attr2][row[1]]){ // table of corses have invalid attrs.
                        csv += row[0] + "," + 
                        dataviva[attr1][row[0]].name.replace(/,/g, '') + "," + 
                        row[1] + "," + 
                        dataviva[attr2][row[1]].name.replace(/,/g, '') + "\n";
                    }
                }
            });

            var a = document.createElement('a');
            a.download = "dataviva-help-crosswalk-" + crosswalk_table + ".csv";
            a.href = 'data:text/csv;charset=utf-8,' + escape(csv);
            a.click();
            
        }
    });
}

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
            dom: 'Bfti',
            "buttons": [ 
                {
                    text: 'save',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    action: function ( e, dt, node, config ) {
                        download('pi', 'hs', 'cnae')
                    }   
                }
            ],
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
            "scrollCollapse": true,
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
            dom: 'Bfti',
            "buttons": [ 
                {
                    text: 'save',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    action: function ( e, dt, node, config ) {
                        download('ip', 'cnae', 'hs')
                    }  
                }
            ],
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
                            return dataviva.cnae[row[0]].name.truncate(40) + ' (' + row[0] + ')';
                        }
                        else{
                            return '-';
                        }

                    }
                },
                {
                    render: function (data, type, row, meta){
                        result = '';
                        $.each(row[1], function(i, value) {
                            if(dataviva.hs[ value ])
                                result += (i != 0 ? '</br>' : '') + dataviva.hs[value].name.truncate(40) + ' (' + value + ')';
                        });
                        return result != '' ? result : "-";
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
                loadingCrosswalkIP.show();
                $('.crosswalk-ip .crosswalk-ip-wrapper .crosswalk-ip-content').show();
                loadingCrosswalkIP.hide();
            }
        });
    };
    window.industryProduct = new IndustryProductTable(loadingCrosswalkIP.hide());
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
            dom: 'Bfti',
            "buttons": [ 
                {
                    text: 'save',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    action: function ( e, dt, node, config ) {
                        download('oc', 'cbo', 'course_sc')
                    }  
                }
            ],
            "ajax": {
                "url": "/help/crosswalk/oc",
                "dataSrc": "data",
                "cache": true,
            },
            "order": [],
            "columns": [
                {
                    render: function (data, type, row, meta){
                            return dataviva.cbo[row[0]].name.truncate(40) + ' (' + row[0] + ')';
                    }
                },
                {
                    render: function (data, type, row, meta){
                        result = '';
                        $.each(row[1], function(i, value) {
                            if(dataviva.course_hedu[ value ])
                                result += (i != 0 ? '</br>' : '') + dataviva.course_hedu[value].name.truncate(40) + ' (' + value + ')';
                            else
                                result += (i != 0 ? '</br>' : '') + dataviva.course_sc[value.substr(1,5)].name.truncate(40) + ' (' + value.substr(1,5) + ')';
                        });

                        return result != '' ? result : "-";
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
            dom: 'Bfti',
            "buttons": [ 
                {
                    text: 'save',
                    text: '<i class="fa fa-floppy-o fa-lg"></i>',
                    action: function ( e, dt, node, config ) {
                        download('co', 'course_sc', 'cbo')
                    }  
                }
            ],
            "ajax": {
                "url": "/help/crosswalk/co",
                "dataSrc": "data",
                "cache": true
            },
            "order": [],
            "columns": [
                {
                    render: function (data, type, row, meta){
                        if(row[0].match(/^[0-9]+$/)){
                           return dataviva.course_sc[row[0].substr(1,5)].name.truncate(40) + ' (' + row[0].substr(1,5) + ')'; 
                        }
                        else if (dataviva.course_hedu[row[0]]){
                            return dataviva.course_hedu[row[0]].name.truncate(40) + ' (' + row[0] + ')';
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
            "scrollCollapse": true,
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

$('.product-industry').on('click', function(){
    dataviva.requireAttrs(['hs', 'cnae'], function() {
        if(!window.productIndustry){
            showCrosswalkPI();
        }
    });
});

$('.industry-product').on('click', function(){
    dataviva.requireAttrs(['hs', 'cnae'], function() {
        if(!window.industryProduct){
            showCrosswalkIP();
        }
    });
});

$('.occupation-course').on('click', function(){
    
    dataviva.requireAttrs(['course_sc', 'cbo', 'course_hedu'], function() {
        if(!window.occupationCourse){    
            showCrosswalkOC();
        }
    });
});

$('.course-occupation').on('click', function(){
    dataviva.requireAttrs(['course_sc', 'cbo', 'course_hedu'], function() {
         if(!window.courseOccupation){
            showCrosswalkCO();
        }
    });
});
