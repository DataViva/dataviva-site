var BlogTable = function () {
    this.tableId = '#blog-table';

    this.table = $(this.tableId).DataTable({
        "sAjaxSource": "/blog/post/all",
        "sAjaxDataProp": "posts",
        "order": [],
        "columnDefs": [
            {
                "targets": 0,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){
                    var checkbox = '<div class="checkbox checkbox-success">' +
                                   '    <input name="selected-item" id="item'+post[0]+'" value="'+post[0]+'" type="checkbox">' +
                                   '    <label for="'+post[0]+'"></label>'
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
                "targets": 4,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, post, meta){
                    if (data){
                       return '<input type="checkbox" class="js-switch" name="activate'+post[0]+'" value="'+post[0]+'" checked>';
                    } else {
                       return '<input type="checkbox" class="js-switch" name="activate'+post[0]+'" value="'+post[0]+'">';
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

var activate = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/blog/admin/activate",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível ativar o(s) post(s) selecionado(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Um ou mais posts selecionados não puderam ser encontrados, a lista de posts será atualizada.', 'info', 8000);
                    blogTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemName = 'activate'+ids[item];
                    if (!$("[name='"+itemName+"']")[0].checked) {
                        $("[name='"+itemName+"']").click();
                    }
                }

                showMessage(message, 'success', 8000);
            }
        });
    } else {
        showMessage('Por favor selecione algum post para ativar.', 'warning', 8000);
    }
}

var deactivate = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/blog/admin/deactivate",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível desativar o(s) post(s) selecionado(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Um ou mais posts selecionados não puderam ser encontrados, a lista de posts será atualizada.', 'info', 8000);
                    blogTable.table.fnReloadAjax();
                }
            },
            success: function (message, textStatus, xhr) {
                for (item in ids) {
                    itemName = 'activate'+ids[item];
                    if ($("[name='"+itemName+"']")[0].checked) {
                        $("[name='"+itemName+"']").click();
                    }
                }
                showMessage(message, 'success', 8000);
            },
        });
    } else {
        showMessage('Por favor selecione para desativar.', 'warning', 8000);
    }
}

var destroy = function(ids){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/blog/admin/delete",
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível excluir o(s) post(s) selecionado(s) devido a um erro no servidor.', 'danger', 8000);
                },
                404: function () {
                    showMessage('Um ou mais posts selecionados não puderam ser encontrados, a lista de posts será atualizada.', 'info', 8000);
                    blogTable.table.fnReloadAjax();
                }
            },
            success: function (message) {
                for (item in ids) {
                    itemId = '#item'+ids[item];
                    blogTable.table.row($(itemId).parents('tr')).remove().draw();
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

var inputThumbCallback = function() {
    $('#thumb-img').hide();
    $('.thumb-buttons').hide();

    $('#thumb-preview').show();
    $('.crop-buttons').show();
    $('.thumb-crop').show();

    $($('#thumb-crop')).cropper({
        aspectRatio: 350/227,
        preview: '#thumb-preview',
        viewMode: 3
    });
}

$(document).ready(function(){

    $('#text-content-editor').append($('#text_content').val())
    $('#text-content-editor').summernote(summernoteConfig);

    $('#blog-edit').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor').summernote(summernoteConfig);
    });

    $('#blog-preview').click(function() {
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

        $('#thumb-img').show();
        $('.thumb-buttons').show();

        $('#thumb-preview').hide();
        $('.crop-buttons').hide();
        $('.thumb-crop').hide();

        $('#thumb-crop').cropper('destroy');
        $('#thumb-crop').attr('src', '');
    });

    $('#admin-delete').click(function() {
        destroy(blogTable.getCheckedIds());
    });
    $('#admin-edit').click(function() {
        edit(blogTable.getCheckedIds());
    });
    $('#admin-activate').click(function() {
        activate(blogTable.getCheckedIds(), true);
    });
    $('#admin-deactivate').click(function() {
        deactivate(blogTable.getCheckedIds(), true);
    });

    var text_max = 500;
    $('#textarea-feedback').html(text_max + ' caracteres restantes');

    $('#text_call').keyup(function() {
        var text_length = $('#text_call').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback').html(text_remaining + ' caracteres restantes');
    });

    $(function() {
        $('#blog-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#text_content').val(aHTML);
            if ($('.summernote').summernote('isEmpty')) {
                $('#text_content').val('');
            }
            return true;
        });
    });

    setAlertTimeOut(8000);
});
