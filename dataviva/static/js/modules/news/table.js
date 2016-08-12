var NewsTable = function () {
    this.tableId = '#news-table';

    $.fn.dataTable.moment('DD/MM/YYYY');

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/news/publication/all",
        "sAjaxDataProp": "publications",
        "order": [[ 3, "asc" ]],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+publication[0]+'" value="'+publication[0]+'" type="checkbox">' +
                                   '    <label for="item'+publication[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 1,
                "className": "column-title",
                "render": function (data, type, publication, meta){
                    return '<a href="/news/publication/'+publication[0]+'">'+publication[1]+'</a>';
                }
            },
            {
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){
                   return '<input type="checkbox" name="show_home" id="show_home'+publication[0]+
                   '" value="'+publication[0]+ (data ? '" checked>' : '" >');
                }
            },
            {
                "targets": 5,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){
                   return '<input type="checkbox" name="active" id="active'+publication[0]+
                   '" value="'+publication[0]+ (data ? '" checked>' : '" >');
                }
            }],
        "paging": false,
        "bFilter": true,
        "info": false,
        "initComplete": function(settings, json) {
            $( 'input[name="show_home"]' ).each(function() {
                var switchery = new Switchery(this, {
                    size: 'small'
                });

                $(this).next().click(function() {
                    var checkbox = $(this).siblings().get(0);

                    var ids = [checkbox.value],
                        status = $(checkbox).attr('name'),
                        status_value = checkbox.checked;

                    changeStatus(ids, status, status_value);
                });
            });

            $( 'input[name="active"]' ).each(function() {
                var switchery = new Switchery(this, {
                    size: 'small',
                    color: '#5A9DC4'
                });

                $(this).next().click(function() {
                    var checkbox = $(this).siblings().get(0);

                    var ids = [checkbox.value],
                        status = $(checkbox).attr('name'),
                        status_value = checkbox.checked;

                    changeStatus(ids, status, status_value);
                });
            });

            $('input[name="selected-item"]').change(function() {
                checkManySelected();
            });
        }
    });

    $('#news-table thead tr th').first().addClass('check-all')

    $('#news-table .check-all').click(function() {
        var checked = $('#news-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

NewsTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#news-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var newsTable = new NewsTable();

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/publication/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) notícia(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais notícias selecionadas não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                    newsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (var i = 0; i < ids.length; i++) {
                    if ($('#'+status+ids[i])[0].checked !== status_value) {
                        $('#'+status+ids[i]).click();
                    }
                }

                showMessage(message, 'success', 8000);
            }
        });
    } else {
        showMessage('Por favor selecione algum post para alterar.', 'warning', 8000);
    }
}

var destroy = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) notícia(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais notícias selecionados não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                    newsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (var i = 0; i < ids.length; i++) {
                    itemId = '#item'+ids[i];
                    newsTable.table.row($(itemId).parents('tr')).remove().draw();
                }

                showMessage(message, 'success', 8000);
            }
        });
    } else {
        showMessage('Por favor selecione para excluir.', 'warning', 8000);
    }
}

var edit = function(ids){
    if (ids.length) {
        window.location = '/'+lang+'/news/admin/publication/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (newsTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}


$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroy(newsTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(newsTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(newsTable.getCheckedIds(), 'active', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(newsTable.getCheckedIds(), 'active', false);
    });

    setAlertTimeOut(8000);
});
