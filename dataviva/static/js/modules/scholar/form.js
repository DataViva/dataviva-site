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
            progressBar.textContent = progressBar.value; // Fallback for unsupported browsers.
        }
    };
    xhr.send(formData); //multipart/form-data
}

function validateFile(){
    if ($('input[type="file"]').val()){
        return true;
    }
    else {
        showMessage('Por favor, insira o arquivo do artigo.', 'danger', 8000);
        return false;
    }
}

$(document).ready(function() {
    $('input[type="file"]').get(0).addEventListener('change', function(e) {
        uploadFiles('/'+window.lang+'/scholar/admin/article/upload', this.files);
    }, false);

    $('#delete').on('click', function (e) {
        var xhr = new XMLHttpRequest();
        xhr.open('DELETE', '/'+window.lang+'/scholar/admin/article/delete', true);
        xhr.onload = function(e) {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    showMessage(xhr.responseText, 'success', 8000);
                    $('#delete').prop('disabled', true);
                } else {
                    showMessage(xhr.statusText, 'danger', 8000);
                    $('#delete').prop('disabled', false);
                }
            }
        };
        xhr.send(csrf_token[0].value);
    });
});
