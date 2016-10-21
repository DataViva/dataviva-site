var ScholarTable = function () {
    this.tableId = '#scholar-table';

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/scholar/admin/articles/all",
        "sAjaxDataProp": "articles",
        "order": [[ 3, "asc" ]],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, articles, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+articles[0]+'" value="'+articles[0]+'" type="checkbox">' +
                                   '    <label for="item'+articles[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 1,
                "className": "column-title",
                "render": function (data, type, articles, meta){
                    return '<a href="/scholar/article/'+articles[0]+'">'+articles[1]+'</a>';
                }
            },
            {
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, articles, meta){
                   return '<input type="checkbox" name="approval_status" id="approval_status'+articles[0]+
                   '" value="'+articles[0]+ (data ? '" checked>' : '" >');
                }
            }],
        "paging": false,
        "bFilter": true,
        "info": false,
        "initComplete": function(settings, json) {
            $( 'input[name="approval_status"]' ).each(function() {
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

    $('#scholar-table thead tr th').first().addClass('check-all')

    $('#scholar-table .check-all').click(function() {
        var checked = $('#scholar-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

ScholarTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#scholar-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var scholarTable = new ScholarTable();

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/scholar/admin/article/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar o(s) artigo(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais artigos selecionados não puderam ser encontrados, a lista de artigos será atualizada.', 'info', 8000);
                    scholarTable.table.fnReloadAjax();
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

var destroyConfirmation = function(ids){
    if (ids.length) {
        swal({ 
            title: 'Você tem certeza?',
            text: 'Você não será capaz de recuperar o(s) artigo(s)!',
            type: 'warning',   showCancelButton: true,
            confirmButtonText: 'Sim, deletar!',
            closeOnConfirm: true
        }, function(){
            destroy(ids);
        });
    } else {
        showMessage('Por favor selecione para excluir.', 'warning', 8000);
    }
}

var destroy = function(ids){
    var deleteLoading = dataviva.ui.loading('#admin-content');
    deleteLoading.text('Excluindo...');
    $.ajax({
        method: "POST",
        url: "/"+lang+"/scholar/admin/article/delete",
        data: {ids:ids},
        statusCode: {
            500: function () {
                showMessage('Não foi possível alterar o(s) artigo(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
            },
            404: function () {
                showMessage('Um ou mais artigos selecionados não puderam ser encontradas, a lista de artigos será atualizada.', 'info', 8000);
                scholarTable.table.fnReloadAjax();
            }
        },
        success: function (message) {
            for (var i = 0; i < ids.length; i++) {
                itemId = '#item'+ids[i];
                scholarTable.table.row($(itemId).parents('tr')).remove().draw();
            }

            showMessage(message, 'success', 8000);
        },
        complete: function() {
            deleteLoading.hide();
        }
    });
}

var edit = function(ids){
    if (ids.length) {
        window.location = '/'+lang+'/scholar/admin/article/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (scholarTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}

$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroyConfirmation(scholarTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(scholarTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(scholarTable.getCheckedIds(), 'approval_status', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(scholarTable.getCheckedIds(), 'approval_status', false);
    });

    setAlertTimeOut(8000);
});
