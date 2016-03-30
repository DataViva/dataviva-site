var NewsTable = function () {
    this.tableId = '#news-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/news/publication/all",
        "sAjaxDataProp": "publications",
        "order": [],
        "aoColumnsDefs": [
            { "data": "publicationselector" },
            { "data": "title" },
            { "data": "authors" },
            { "data": "publicationDate" },
            { "data": "active" },
        ],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){

                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+publication[0]+'" value="'+publication[0]+'" type="checkbox">' +
                                   '    <label for="'+publication[0]+'"></label>'
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
                    if (data){
                       return '<input type="checkbox" class="js-switch" name="activate'+publication[0]+'" value="'+publication[0]+'" checked>';
                    }
                    else {
                       return '<input type="checkbox" class="js-switch" name="activate'+publication[0]+'" value="'+publication[0]+'">';
                    }
                }
              }],
        "columns": [
                { "width": "8%" },
                null,
                null,
                { "width": "20%" },
                { "width": "12%" }
        ],
        "paging": false,
        "bFilter": false,
        "info": false,
        "initComplete": function(settings, json) {
            $( ".js-switch" ).each(function() {
                var switchery = new Switchery(this, {
                    size: 'small',
                    color: '#5A9DC4'
                });

                $(this).next().click(function() {
                    if($(this).siblings().get(0).checked) {
                        activate($(this).siblings().get(0).value);
                    } else {
                        deactivate($(this).siblings().get(0).value);
                    }
                });
            });
        }
    });

    $('#news-table thead tr th').first().addClass('check-all')

    $('#news-table .check-all').click(function() {
        var checked = $('#news-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
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

var activate = function(ids, refreshButtons){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/activate",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível ativar a(s) publicações(s) selecionada(s) devido a um erro no servidor.', 'danger');
                },
                404: function () {
                    showMessage('Uma ou mais publicações selecionadas não puderam ser encontradas, a lista de publicações será atualizada.', 'info');
                    newsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemName = 'activate'+ids[item];
                    if (!$("[name='"+itemName+"']")[0].checked) {
                        $("[name='"+itemName+"']").click();
                    }
                }

                showMessage(message, 'success');
            }
        });
    } else {
        showMessage('Selecione alguma publicação para ativá-la.', 'warning');
    }
}

var deactivate = function(ids, refreshButtons){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/deactivate",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível excluir a(s) publicações(s) selecionada(s) devido a um erro no servidor.', 'danger');
                },
                404: function () {
                    showMessage('Uma ou mais publicações selecionados não puderam ser encontradas, a lista de publicações será atualizada.', 'info');
                    newsTable.table.fnReloadAjax();
                }
            },
            success: function (message, textStatus, xhr) {
                for (item in ids) {
                    itemName = 'activate'+ids[item];
                    if ($("[name='"+itemName+"']")[0].checked) {
                        $("[name='"+itemName+"']").click();
                    }
                }

                showMessage(message, 'success');
            },
        });
    } else {
        showMessage('Selecione alguma publicação para desativá-lo.', 'warning');
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
                    showMessage('Não foi possível excluir a(s) publicações(s) selecionada(s) devido a um erro no servidor.', 'danger');
                },
                404: function () {
                    showMessage('Uma ou mais publicações selecionados não puderam ser encontradas, a lista de publicações será atualizada.', 'info');
                    newsTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemId = '#item'+ids[item];
                    newsTable.table.row($(itemId).parents('tr')).remove().draw();
                }

                showMessage(message, 'success');
            }
        });
    } else {
        showMessage('Selecione alguma publicação para excluí-lo.', 'warning');
    }
}

var edit = function(ids){
    if (ids.length) {
        window.location = '/'+lang+'/news/admin/publication/'+ids[0]+'/edit';
    } else {
        showMessage('Selecione alguma publicação para editá-la.', 'warning');
    }
}

var inputThumbCallback = function() {
    $($('#thumb-crop')).cropper({
        aspectRatio: 350/227,
        preview: '#thumb-preview',
        viewMode: 3
    });

    $('#thumb-img').hide();
    $('#thumb-crop').show();
    $('.thumb .crop-controls').show();
    $('.thumb label').hide();
}

$(document).ready(function(){

    $('#text-content-editor').append($('#text_content').val())
    $('#text-content-editor').summernote(summernoteConfig);

    $('#news-edit').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor').summernote(summernoteConfig);
    });

    $('#news-preview').click(function() {
        var aHTML = $('#text-content-editor').summernote('code');
        $('#text_content').val(aHTML);
        $('#text-content-editor').summernote('destroy');
    });

    cropInput($('#thumb-crop'), $('#thumb-input'), inputThumbCallback)

    $('#thumb-zoomIn').click(function() {
        $('#thumb-crop').cropper('zoom', 0.1);
    });
    $('#thumb-zoomOut').click(function() {
        $('#thumb-crop').cropper('zoom', -0.1);
    });
    $('#thumb-rotateLeft').click(function() {
        $('#thumb-crop').cropper('rotate', 45);
    });
    $('#thumb-rotateRight').click(function() {
        $('#thumb-crop').cropper('rotate', -45);
    });
    $('#thumb-save').click(function() {
        var thumbDataURL = $('#thumb-crop').cropper('getDataURL');
        $('#thumb').val(thumbDataURL);
        $('#thumb-img').attr('src', thumbDataURL);
        $('#thumb-crop').cropper('destroy');
        $('#thumb-crop').attr('src', '');
        $('#thumb-img').show();
        $('.thumb label').show();
        $('.thumb .crop-controls').hide();
    });

    $('#admin-delete').click(function() {
        destroy(newsTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(newsTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        activate(newsTable.getCheckedIds(), true);
    });
    $('#admin-deactivate').click(function() {
        deactivate(newsTable.getCheckedIds(), true);
    });

    $(function() {
        $('#news-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#text_content').val(aHTML);
            return true;
        });
    });
});
