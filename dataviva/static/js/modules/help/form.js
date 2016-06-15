$(document).ready(function(){

    //Summernote for answer-en
    $('#text-content-editor-en').append($('#answer_en').val())
    $('#text-content-editor-en').summernote(summernoteConfig);

    $('#help-edit-en').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor-en').summernote(summernoteConfig);
    });

    $('#help-preview-en').click(function() {
        var aHTML = $('#text-content-editor-en').summernote('code');
        $('#answer_en').val(aHTML);
        $('#text-content-editor-en').summernote('destroy');
    });

    var text_max = 500;
    $('#textarea-feedback-en').html(text_max + ' caracteres restantes');

    $('#text_call-en').keyup(function() {
        var text_length = $('#text_call-en').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback-en').html(text_remaining + ' caracteres restantes');
    });

    $(function() {
        $('#help-form').submit(function() {
            var aHTML = $('#text-content-editor-en').summernote('code');
            $('#answer_en').val(aHTML);
            if ($('.summernote').summernote('isEmpty')) {
                $('#answer_en').val('');
            }
            return true;
        });
    });

    //Summernote for answer-pr
    $('#text-content-editor-pt').append($('#answer_pt').val())
    $('#text-content-editor-pt').summernote(summernoteConfig);

    $('#help-edit-pt').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor-pt').summernote(summernoteConfig);
    });

    $('#help-preview-pt').click(function() {
        var aHTML = $('#text-content-editor-pt').summernote('code');
        $('#answer_pt').val(aHTML);
        $('#text-content-editor-pt').summernote('destroy');
    });

    var text_max = 500;
    $('#textarea-feedback-pt').html(text_max + ' caracteres restantes');

    $('#text_call-pt').keyup(function() {
        var text_length = $('#text_call-pt').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback-pt').html(text_remaining + ' caracteres restantes');
    });

    $(function() {
        $('#help-form').submit(function() {
            var aHTML = $('#text-content-editor-pt').summernote('code');
            $('#answer_pt').val(aHTML);
            if ($('.summernote').summernote('isEmpty')) {
                $('#answer_pt').val('');
            }
            return true;
        });
    });
});
