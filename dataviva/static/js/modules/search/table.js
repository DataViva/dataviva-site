var SearchTable = function () {
    this.tableId = '#search-table';

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/search/question/all",
        "sAjaxDataProp": "questions",
        "order": [],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, question, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+question[0]+'" value="'+question[0]+'" type="checkbox">' +
                                   '    <label for="'+question[0]+'"></label>'
                                   '</div>';

                    return checkbox;
                }
            },{
                "targets": 3,
                "render": function(data, type, question, meta){
                    return data.join(", ") ;   
                }
            }
            ],
        "paging": false,
        "bFilter": true,
        "info": false,
        "initComplete": function(settings, json) {
            $('input[name="selected-item"]').change(function() {
                checkManySelected();
            });
        }
    });

    $('#search-table thead tr th').first().addClass('check-all')

    $('#search-table .check-all').click(function() {
        var checked = $('#search-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
    })
};

SearchTable.prototype.getCheckedIds = function(first_argument) {
    var checkedIds = [];
    $('#search-table input[name="selected-item"]').each(function() {
        if (this.checked) {
            checkedIds.push(this.value);
        }
    });
    return checkedIds;
};

var searchTable = new SearchTable();

var destroy = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/search/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) questão(ões) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Uma ou mais questões selecionados não puderam ser encontradas, a lista de questões será atualizada.', 'info', 8000);
                    searchTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemId = '#item'+ids[item];
                    searchTable.table.row($(itemId).parents('tr')).remove().draw();
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
        window.location = '/'+lang+'/search/admin/question/'+ids[0]+'/edit';
    } else {
        showMessage('Por favor selecione para editar.', 'warning', 8000);
    }
}

var checkManySelected = function() {
    if (searchTable.getCheckedIds().length > 1) {
        $('#admin-edit').prop('disabled', true);
    } else {
        $('#admin-edit').prop('disabled', false);
    }
}


$(document).ready(function(){
    $('#admin-delete').click(function() {
        destroy(searchTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(searchTable.getCheckedIds());
    });

    setAlertTimeOut(8000);
});
