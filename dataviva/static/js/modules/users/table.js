var UserTable = function () {
    this.tableId = '#users-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/users/all",
        "sAjaxDataProp": "users",
        "order": [],
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
                "targets": 1,
                "className": "column-title",
                "render": function (data, type, users, meta){
                    return '<a href="/blog/users/'+users[0]+'">'+users[1]+'</a>';
                }
            },
            {
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, users, meta){
                    if (data){
                       return '<input type="checkbox" class="js-switch" name="activate'+users[0]+'" value="'+users[0]+'" checked>';
                    } else {
                       return '<input type="checkbox" class="js-switch" name="activate'+users[0]+'" value="'+users[0]+'">';
                    }
                }
              }],
        "paging": false,
        "bFilter": true,
        "info": false,
        "initComplete": function(settings, json) {
            $( ".js-switch" ).each(function() {
                var switchery = new Switchery(this, {
                    size: 'small',
                    color: '#5A9DC4'
                });

                $(this).next().click(function() {
                    if($(this).siblings().get(0).checked) {
                        activate([$(this).siblings().get(0).value]);
                    } else {
                        deactivate([$(this).siblings().get(0).value]);
                    }
                });
            });

            $('input[name="selected-item"]').change(function() {
                checkManySelected();
            });
        }
    });

    $('#blog-table thead tr th').first().addClass('check-all')

    $('#blog-table .check-all').click(function() {
        var checked = $('#blog-table .check-all input:checkbox').get(0).checked;
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
        showMessage('Por favor selecione algum users para alterar.', 'warning', 8000);
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
