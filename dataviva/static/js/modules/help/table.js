var HelpTable = function () {
    this.tableId = '#help-table';

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/help/subject/all",
        "sAjaxDataProp": "subjects",
        "order": [[ 3, "asc" ]],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, subject, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+subject[0]+'" value="'+subject[0]+'" type="checkbox">' +
                                   '    <label for="item'+subject[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 2,
                "className": "column-title",
                "render": function (data, type, subject, meta){
                    return '<a href="/help/subject/'+subject[0]+'">'+subject[2]+'</a>';
                }
            },
            {
                "targets": 3,
                "className": "column-title",
                "render": function (data, type, subject, meta){
                    return subject[3].truncate(300);
                }
            },
            {
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, subject, meta){
                   return '<input type="checkbox" name="active" id="active'+subject[0]+
                   '" value="'+subject[0]+ (data ? '" checked>' : '" >');
                }
            }],
        "paging": false,
        "bFilter": true,
        "info": false,
        "initComplete": function(settings, json) {
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

    $('#help-table thead tr th').first().addClass('check-all')

    $('#help-table .check-all').click(function() {
        var checked = $('#help-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

HelpTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#help-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var helpTable = new HelpTable();

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/help/admin/subject/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) pergunta(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais perguntas selecionadas não puderam ser encontradas, a lista de perguntas será atualizada.', 'info', 8000);
                    helpTable.table.fnReloadAjax();
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
        showMessage('Por favor selecione alguma pergunta para alterar.', 'warning', 8000);
    }
}

var destroy = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/help/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) perguntas(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais perguntas selecionados não puderam ser encontradas, a lista de perguntas será atualizada.', 'info', 8000);
                    helpTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (var i = 0; i < ids.length; i++) {
                    itemId = '#item'+ids[i];
                    helpTable.table.row($(itemId).parents('tr')).remove().draw();
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
        window.location = '/'+lang+'/help/admin/subject/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (helpTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}

$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroy(helpTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(helpTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(helpTable.getCheckedIds(), 'active', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(helpTable.getCheckedIds(), 'active', false);
    });

    setAlertTimeOut(8000);
});
