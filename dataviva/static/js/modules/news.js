$(document).ready(function(){
    var lang = document.documentElement.lang

    if (lang == 'pt') {
        lang = 'pt-BR';
    } else if (lang == 'en') {
        lang = 'en-US';
    }

    var summernoteConfig = {
        lang: lang,
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['table', ['table']],
            ['insert', ['link', 'picture', 'video']],
            ['view', ['fullscreen', 'codeview', 'help']]
          ],
        fontNames: [
            'Arial', 'Arial Black', 'Comic Sans MS', 'Courier New',
            'Helvetica Neue', 'Helvetica', 'Impact', 'Lucida Grande',
            'Open Sans', 'Tahoma', 'Times New Roman', 'Verdana'
          ],
        placeholder: 'Escreva aqui o conteúdo desta publicação'
    }

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

    $(function() {
        $('#news-form').submit(function() {
            var aHTML = $('#text-content-editor').summernote('code');
            $('#text_content').val(aHTML);
            return true;
        });
    });
});
