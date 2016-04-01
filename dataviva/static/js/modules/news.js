var NewsTable = function () {
    this.tableId = '#news-table';

    this.table = $(this.tableId).DataTable({
        "oLanguage": {
          "sSearch": "Pesquisar "
        },
        "sAjaxSource": "/news/publication/all",
        "sAjaxDataProp": "publications",
        "order": [],
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
                   return '<input type="checkbox" name="show_home" id="show_home'+publication[0]+
                   '" value="'+publication[0]+ (data ? '" checked>' : '" >');
                }
            },
            {
                "targets": 5,
                "orderable": false,
                "className": "column-checkbox",
                "render": function (data, type, publication, meta){
                   return '<input type="checkbox" name="active" id="active'+publication[0]+
                   '" value="'+publication[0]+ (data ? '" checked>' : '" >');
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

    $('#news-table thead tr th').first().addClass('check-all')

    $('#news-table .check-all').click(function() {
        var checked = $('#news-table .check-all input:checkbox').get(0).checked;
        $('input[name="selected-item"]').each(function() {
            $(this).prop('checked', checked);
        });
        checkManySelected();
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

var changeStatus = function(ids, status, status_value){
    if (ids.length) {
        $.ajax({
            method: "POST",
            url: "/"+lang+"/news/admin/publication/"+status+"/"+status_value,
            data: {ids:ids},
            statusCode: {
                500: function () {
                    showMessage('Não foi possível alterar a(s) notícia(s) selecionada(s) devido a um erro no servidor.', 'danger', 8000);
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
        window.location = '/'+lang+'/news/admin/publication/'+ids[0]+'/edit';
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

        $('#thumb-img').show();
        $('.thumb-buttons').show();

        $('#thumb-preview').hide();
        $('.crop-buttons').hide();
        $('.thumb-crop').hide();

        $('#thumb-crop').cropper('destroy');
        $('#thumb-crop').attr('src', '');
    });


    $('#publish-date').datepicker({
        format: "dd/mm/yyyy",
        todayBtn: "linked",
        keyboardNavigation: false,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });

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

    var text_max = 500;
    $('#textarea-feedback').html(text_max + ' caracteres restantes');

    $('#text_call').keyup(function() {
        var text_length = $('#text_call').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback').html(text_remaining + ' caracteres restantes');
    });

    $(function() {
        $('#news-form').submit(function() {
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
