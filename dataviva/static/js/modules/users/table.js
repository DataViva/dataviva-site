var UsersTable = function () {
    this.tableId = '#users-table';

    this.table = $('#users-table').DataTable( {
                "sAjaxSource": "/users/all",
                "sAjaxDataProp": "users",
                "order": [],
                "columns": [
                    null,
                    {data: 0},
                    {data: 1},
                    {data: 2},
                    {data: 3}
                ],
                "columnDefs": [ 
                    {
                        "targets": 0,
                        "orderable": false,
                        "className": "column-checkbox",
                        "render": function (data, type, users, meta){
                            var checkbox = '<div class="checkbox checkbox-success">' +
                                           '    <input name="selected-item" id="item'+users[0]+'" value="'+users[0]+'" type="checkbox">' +
                                           '    <label for="'+users[0]+'"></label>'
                                           '</div>';

                        return checkbox;
                    }
                    },
                    {
                        'className' : 'body-checkbox',
                        'targets':  4,
                        'render': function(data, type, users, meta){
                            return '<input type="checkbox" name="active" id="active'+users[0]+
                                    '" value="'+users[0]+ (data ? '" checked>' : '" >');
                    },
                } ],             
               "paging": true,
               "bFilter": false,
               "info": false, //number of rows in footer table
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

    $('#users-table thead tr th').first().addClass('check-all')

    $('#users-table .check-all').click(function() {
        var checked = $('#users-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

UsersTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#users-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var usersTable = new UsersTable();

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/users/admin/users/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar o(s) usuário(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Um ou mais usuários selecionados não puderam ser encontrados, a lista de usuários será atualizada.', 'info', 8000);
                    usersTable.table.fnReloadAjax();
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
        showMessage('Por favor selecione algum usuário para alterar.', 'warning', 8000);
    }
}

var destroy = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/users/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar o(s) usuário(s) selecionado(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Um ou mais usuários selecionados não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                    usersTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemId = '#item'+ids[item];
                    usersTable.table.row($(itemId).parents('tr')).remove().draw();
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
        window.location = '/'+lang+'/users/admin/users/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (usersTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}


$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroy(usersTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(usersTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(usersTable.getCheckedIds(), 'active', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(usersTable.getCheckedIds(), 'active', false);
    });

    setAlertTimeOut(8000);
});
