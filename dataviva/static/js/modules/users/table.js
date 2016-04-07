var UsersTable = function () {
    this.tableId = '#users-table';

    this.table = $('#users-table').DataTable( {
                "sAjaxSource": "/users/all",
                "sAjaxDataProp": "users",
                "aoColumnsDefs": [
                    { "data": "id" },
                    { "data": "title" },
                    { "data": "authors" },
                    { "data": "role"},
                ],
                "columnDefs": [ {
                    'className' : 'body-checkbox',
                    'targets':   3,
                    'render': function(data, type,users, meta){
                        if(data){
                            return '<input type="checkbox" name="checkboxAdmin" value="'+users[0]+'" checked>'
                        }else{
                            return '<input type="checkbox" name="checkboxAdmin" value="'+users[0]+'">'
                        }
                    }
                } ],
                "columns": [
                   { "width": "10%" },
                   { "width": "30%" },
                   null,
                   { "width": "19%" },
                 ],              
               "paging": false,
               "bFilter": false,
               "info": false //number of rows in footer table
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

var newsTable = new UsersTable();

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/users/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar o(s) usuário(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais notícias selecionadas não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                    newsTable.table.fnReloadAjax();
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
                for (item in ids) {
                    itemId = '#item'+ids[item];
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
        window.location = '/'+lang+'/news/admin/users/'+ids[0]+'/edit';
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
