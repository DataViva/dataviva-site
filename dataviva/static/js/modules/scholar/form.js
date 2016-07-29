
var path = window.location.pathname.split('/');
if (path[path.length - 1] === 'new'){
    $('#uploaded-file').hide();
    $('#progress').hide();
}

else if (path[path.length - 1] === 'edit'){
    var articleId = path[path.length - 2];
    $('#input-file').hide();
    $('#progress').hide();
    $('#delete').attr('id', 'delete-edit');
    $('#article-url').attr('href', dataviva.s3_host + '/scholar/'+articleId+'/files/article');
}


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


$('#file').get(0).addEventListener('change', function(e) {
    if ($('#file').val().split('.').pop().toLowerCase() !== 'pdf'){
        $('#file').val('');
        showMessage('Tipo de arquivo não suportado, favor inserir um arquivo PDF.', 'danger', 8000);
        return false;
    }
    else if ($('#file')[0].files[0].size/1024/1024 > 50){
            $('#file').val('');
            showMessage('Não foi possível salvar o arquivo, favor inserir um arquivo de no máximo 50 MB.', 'danger', 8000);
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

