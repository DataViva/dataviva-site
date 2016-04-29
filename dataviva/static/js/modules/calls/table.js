var CallsTable = function () {
    this.tableId = '#calls-table';

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/calls/all",
        "sAjaxDataProp": "calls",
        "order": [],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, call, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+call[0]+'" value="'+call[0]+'" type="checkbox">' +
                                   '    <label for="'+call[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 2,
                "className": "column-title",
                "render": function (data, type, call, meta){
                    return "<a href='"+call[2]+"' target='_blank'>"+call[2]+"</a>";
                }
            },
            {
                "targets": 3,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, call, meta){
                   return '<input type="checkbox" name="active" id="active'+call[0]+
                   '" value="'+call[0]+ (data ? '" checked>' : '" >');
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

    $('#calls-table thead tr th').first().addClass('check-all')

    $('#calls-table .check-all').click(function() {
        var checked = $('#calls-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

CallsTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#calls-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};


var callsTable = new CallsTable();


var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/calls/admin/call/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) chamada(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais chamadas selecionadas não puderam ser encontradas, a lista de chamadas será atualizada.', 'info', 8000);
                    callsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    if ($('#'+status+ids[item])[0].checked !== status_value) {
                        $('#'+status+ids[item]).click();
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
            url: "/"+lang+"/calls/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) chamada(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais chamadas selecionados não puderam ser encontradas, a lista de chamadas será atualizada.', 'info', 8000);
                    callsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemId = '#item'+ids[item];
                    callsTable.table.row($(itemId).parents('tr')).remove().draw();
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
        window.location = '/'+lang+'/calls/admin/call/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (callsTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}

$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroy(callsTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(callsTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(callsTable.getCheckedIds(), 'active', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(callsTable.getCheckedIds(), 'active', false);
    });

    setAlertTimeOut(8000);
});
