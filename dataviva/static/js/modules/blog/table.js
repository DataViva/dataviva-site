var BlogTable = function () {
    this.tableId = '#blog-table';

    $.fn.dataTable.moment('DD/MM/YYYY');

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/blog/post/all",
        "sAjaxDataProp": "posts",
        "order": [[ 3, "asc" ]],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+post[0]+'" value="'+post[0]+'" type="checkbox">' +
                                   '    <label for="item'+post[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },
            {
                "targets": 1,
                "className": "column-title",
                "render": function (data, type, post, meta){
                    return '<a href="/blog/post/'+post[0]+'">'+post[1]+'</a>';
                }
            },
            {
                "targets": 5,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){
                   return '<input type="checkbox" name="show_home" id="show_home'+publication[0]+
                   '" value="'+publication[0]+ (data ? '" checked>' : '" >');
                }
            },
            {
                "targets": 6,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){
                   return '<input type="checkbox" name="active" id="active'+post[0]+
                   '" value="'+post[0]+ (data ? '" checked>' : '" >');
                }
            }
        ],
        "buttons": [
            {
                text: "<i class='fa fa-clock-o'></i>",
                className: 'btn btn-sm btn-white',
                titleAttr: 'Histórico de operações',
                action: function (e, dt, node, config) {
                    $('#logs-download-modal').modal('show');
                    initLogsDownload('blog');
                }
            }
        ],
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

            $('#blog-table_wrapper .col-sm-6:eq(1)').addClass('text-right');
            $('#blog-table').dataTable().api().buttons().container().appendTo('#blog-table_wrapper .col-sm-6:eq(1)');
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

BlogTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#blog-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var blogTable = new BlogTable();

var changeStatus = function(ids, status, status_value) {
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/blog/admin/post/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) notícia(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais notícias selecionadas não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                    blogTable.table.fnReloadAjax();
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
            text: 'Você não será capaz de recuperar o(s) post(s)!',
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
        url: "/"+lang+"/blog/admin/delete",
        data: {ids: ids},
        statusCode: {
            500: function () {
                showMessage('Não foi possível alterar a(s) notícia(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
            },
            404: function () {
                showMessage('Uma ou mais notícias selecionados não puderam ser encontradas, a lista de notícias será atualizada.', 'info', 8000);
                blogTable.table.fnReloadAjax();
            }
        },
        success: function (message) {
            for (var i = 0; i < ids.length; i++) {
                itemId = '#item'+ids[i];
                blogTable.table.row($(itemId).parents('tr')).remove().draw();
            }
                
            showMessage(message, 'success', 8000);
        },
        complete: function() {
            deleteLoading.hide();
        }
    });
}

var edit = function(ids) {
    if (ids.length) {
        window.location = '/'+lang+'/blog/admin/post/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (blogTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}

$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroyConfirmation(blogTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(blogTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        changeStatus(blogTable.getCheckedIds(), 'active', true);
    });
    $('#admin-deactivate').click(function() {
        changeStatus(blogTable.getCheckedIds(), 'active', false);
    });

    setAlertTimeOut(8000);
});
