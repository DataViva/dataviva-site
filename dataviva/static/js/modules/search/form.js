$(document).ready(function(){

    $('#text-content-editor').append($('#answer').val())
    $('#text-content-editor').summernote(summernoteConfig);

    $('#search-edit').click(function() {
        summernoteConfig['focus'] = true;
        $('#text-content-editor').summernote(summernoteConfig);
    });

    $('#search-preview').click(function() {
        var aHTML = $('#text-content-editor').summernote('code');
        $('#answer').val(aHTML);
        $('#text-content-editor').summernote('destroy');
    });

    var text_max = 500;
    $('#textarea-feedback').html(text_max + ' caracteres restantes');

    $('#text_call').keyup(function() {
        var text_length = $('#text_call').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback').html(text_remaining + ' caracteres restantes');
    });

    $(function() {
        $('#search-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#answer').val(aHTML);
            if ($('.summernote').summernote('isEmpty')) {
                $('#answer').val('');
            }
            return true;
        });
    });
});