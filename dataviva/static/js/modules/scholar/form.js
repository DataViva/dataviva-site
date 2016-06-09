function uploadFiles(url, files) {
    var formData = new FormData();
    var file = files[0];
    formData.append(file.name, file);
    formData.append('csrf_token', csrf_token[0].value);
    var xhr = new XMLHttpRequest();
    xhr.open('POST', url, true);
    xhr.onload = function(e) {
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
    xhr.upload.onprogress = function(e) {
        if (e.lengthComputable) {
            progressBar.value = (e.loaded / e.total) * 100;
            progressBar.textContent = progressBar.value; //Fallback for unsupported browsers.
        }
    };
    xhr.send(formData); //multipart/form-data
}

function validateFile(){
    if ($('#file').val()){
        return true;
    }
    else {
        showMessage('Por favor, insira o arquivo do artigo.', 'danger', 8000);
        return false;
    }
}

if (window.location.pathname.split('/').pop() === 'new'){
    $('#uploaded-file').hide();
    $('#progress').hide();
}

if (window.location.pathname.split('/').pop() === 'edit'){
    var path = window.location.pathname.split('/');
    var articleId = path[path.length-2];
    $('#input-file').hide();
    $('#progress').hide();
    $('#uploaded-file').empty();
    $('#uploaded-file').append('<button href="#" class="btn btn-danger" id="delete-edit">' + 
                                        '<i class="fa fa-trash-o m-r-sm"></i> Delete File ' +
                                '</button>' +
                                '<a id="article-url" href="https://dataviva-dev.s3.amazonaws.com/scholar/'+articleId+'/files/article" target="_blank"> Artigo <i class="fa fa-file-pdf-o m-r-sm"></i></a>'
                                )
}

$(document).ready(function() {
    $('#file').get(0).addEventListener('change', function(e) {
        if ($('#file').val().split('.').pop().toLowerCase() !== 'pdf'){
            $('#file').val('');
            showMessage('Tipo de arquivo não suportado.', 'danger', 8000);
            return false;
        }
        else if ($('#file')[0].files[0].size/1024/1024 > 50){
                $('#file').val('');
                showMessage('Arquivo deve possuir no máximo 50MB.', 'danger', 8000);
                return false;
        }
        else {
            $('#progress').show();
            uploadFiles('/'+window.lang+'/scholar/admin/article/upload', this.files);
            $('#article-url').attr('href', '/scholar/admin/file/'+csrf_token[0].value.substring(0,10)+'/'+csrf_token[0].value.substring(12,52));
            $('#input-file').hide();
            $('#uploaded-file').show();
            $('#progress').hide();
        }
    }, false);

    $('#delete').on('click', function (e) {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/'+window.lang+'/scholar/admin/article/delete', true);
        xhr.onload = function(e) {
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

    $('#delete-edit').on('click', function (e) {
        $('#file').val('');
        showMessage('File Removed!', 'success', 8000);
        $('#uploaded-file').hide();
        $('#input-file').show();
    });
});
