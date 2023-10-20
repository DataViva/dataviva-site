var inputThumbCallback = function () {
    $('#thumb-img').hide();
    $('.thumb-buttons').hide();

    $('#thumb-preview').show();
    $('.crop-buttons').show();
    $('.thumb-crop').show();

    $($('#thumb-crop')).cropper({
        aspectRatio: 230 / 360, // Aspect ratio vertical (100px de altura por 330px de largura)
        preview: '#thumb-preview',
        viewMode: 3
    });
}

$(document).ready(function () {
    var path = window.location.pathname.split('/');

    if (path[path.length - 1] === 'new') {
        $('#uploaded-file').hide();
        $('#progress').hide();
    } else if (path[path.length - 1] === 'edit') {
        var articleId = path[path.length - 2];
        $('#input-file').hide();
        $('#progress').hide();
        $('#delete').attr('id', 'delete-edit');
        $('#article-url').attr('href', 'https://' + dataviva.s3_bucket + '.s3.amazonaws.com/scholar/' + articleId + '/files/article');
    }

    select2Config.placeholder = 'Separe as palavras-chave por vírgula';
    $('#keywords').select2(select2Config);

    var scholarSummernoteConfig = {
        lang: lang_code,
        height: 200,
        fontNames: [
            'Arial', 'Arial Black', 'Comic Sans MS', 'Courier New',
            'Helvetica Neue', 'Helvetica', 'Impact', 'Lucida Grande',
            'Open Sans', 'Tahoma', 'Times New Roman', 'Verdana'
        ],
        toolbar: [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['view', ['fullscreen', 'codeview', 'help']]
        ]
    };

    cropInput($('#thumb-crop'), $('#thumb-input'), inputThumbCallback)

    $('#thumb-zoomIn').click(function () {
        $('#thumb-crop').cropper('zoom', 0.1);
    });
    $('#thumb-zoomOut').click(function () {
        $('#thumb-crop').cropper('zoom', -0.1);
    });
    $('#thumb-rotateLeft').click(function () {
        $('#thumb-crop').cropper('rotate', 45);
    });
    $('#thumb-rotateRight').click(function () {
        $('#thumb-crop').cropper('rotate', -45);
    });
    $('#thumb-save').click(function () {
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

    $('#abstract-edit').click(function () {
        var editor = $('#text-content-editor');
        $('#abstract-preview').prop('disabled', false);
        $('#abstract-edit').prop('disabled', true);
        scholarSummernoteConfig['focus'] = true;
        editor.summernote(scholarSummernoteConfig);
    });

    $('#abstract-preview').click(function () {
        var editor = $('#text-content-editor');
        $('#abstract-preview').prop('disabled', true);
        $('#abstract-edit').prop('disabled', false);
        editor.summernote('destroy');
        var aHTML = editor.html();
        $('text_content').val(aHTML);
    });

    $('#abstract-edit').prop('disabled', true);

    $('#text-content-editor').append($('#text_content').val());
    $('#text-content-editor').summernote(scholarSummernoteConfig);

    function uploadFiles(url, files) {
        var formData = new FormData();
        var file = files[0];
        formData.append(file.name, file);
        formData.append('csrf_token', csrf_token[0].value);
        var xhr = new XMLHttpRequest();
        xhr.open('POST', url, true);
        xhr.onload = function (e) {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    showMessage(xhr.responseText, 'success', 8000);
                    $('#delete').prop('disabled', false);
                } else {
                    showMessage(xhr.statusText, 'danger', 8000);
                    $('#delete').prop('disabled', true);
                }
            }
        };
        var progressBar = document.querySelector('progress');
        xhr.upload.onprogress = function (e) {
            if (e.lengthComputable) {
                progressBar.value = (e.loaded / e.total) * 100;
                progressBar.textContent = progressBar.value; //Fallback for unsupported browsers.
            }
        };
        xhr.send(formData); //multipart/form-data
    }


    $('#file').get(0).addEventListener('change', function (e) {
        if ($('#file').val().split('.').pop().toLowerCase() !== 'pdf') {
            $('#file').val('');
            showMessage('Tipo de arquivo não suportado, favor inserir um arquivo PDF.', 'danger', 8000);
            return false;
        }
        else if ($('#file')[0].files[0].size / 1024 / 1024 > 50) {
            $('#file').val('');
            showMessage('Não foi possível salvar o arquivo, favor inserir um arquivo de no máximo 50 MB.', 'danger', 8000);
            return false;
        }
        else {
            $('#progress').show();
            uploadFiles('/' + window.lang + '/scholar/admin/article/upload', this.files);
            $('#article-url').attr('href', '/scholar/admin/file/' + csrf_token[0].value.substring(0, 10) + '/' + csrf_token[0].value.substring(12, 52));
            $('#input-file').hide();
            $('#uploaded-file').show();
            $('#progress').hide();
        }
    }, false);


    $('#delete').on('click', function (e) {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/' + window.lang + '/scholar/admin/article/delete', true);
        xhr.onload = function (e) {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    showMessage(xhr.responseText, 'success', 8000);
                    $('#file').val('');
                    $('#uploaded-file').hide();
                    $('#input-file').show();
                } else {
                    showMessage(xhr.statusText, 'danger', 8000);
                }
            }
        };
        xhr.send(csrf_token[0].value);
    });

    document.getElementById("image").addEventListener("change", function () {
        var input = this;
        var img = document.getElementById("uploaded-image");

        if (input.files && input.files[0]) {
            var reader = new FileReader();

            reader.onload = function (e) {
                var base64Image = e.target.result;
                img.src = base64Image;
            };

            reader.readAsDataURL(input.files[0]);
        }
    });

    $('#delete-edit').on('click', function (e) {
        $('#file').val('');
        showMessage('File Removed!', 'success', 8000);
        $('#uploaded-file').hide();
        $('#input-file').show();
    });
});

