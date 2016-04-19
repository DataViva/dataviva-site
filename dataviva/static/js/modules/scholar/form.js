$(function () {
    'use strict';

    $('#fileupload').fileupload({
        url: 'upload'
    });

    $('#fileupload').fileupload({
        submit: function (e, data) {
            var $this = $(this);
            //data.formData['csrf_token'] = $('#csrf_token').val();
            data.jqXHR = $this.fileupload('send', data);
        }
    });

    // Load existing files:
    $('#fileupload').addClass('fileupload-processing');
    $.ajax({
        // Uncomment the following to send cross-domain cookies:
        //xhrFields: {withCredentials: true},
        url: $('#fileupload').fileupload('option', 'url'),
        dataType: 'json',
        context: $('#fileupload')[0]
    }).always(function () {
        $(this).removeClass('fileupload-processing');
    }).done(function (result) {
        $(this).fileupload('option', 'done')
            .call(this, $.Event('done'), {result: result});
    });

});
