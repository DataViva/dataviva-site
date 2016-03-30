$(document).ready(function () {
    new WOW().init();
    $("[data-toggle=popover]").popover({ trigger: "hover" });
    $('.counter').counterUp();
    $.stellar();

    $( ".js-switch" ).each(function() {
      var switchery = new Switchery(this);
    });

    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/pt_BR/sdk.js#xfbml=1&version=v2.5&appId=222520191136295";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));


});

function setAlertTimeOut(time) {
    window.setTimeout(function() {
      $(".alert").fadeTo(500, 0).slideUp(500, function(){
          $(this).remove();
      });
    }, time);
}

function showMessage(message, category, timeout) {
    if (category == null) {
        category = 'info';
    }
    $('#message').append(
        '<div class="alert alert-' + category + ' alert-dismissable animated fadeInDown">' +
        '<button aria-hidden="true" data-dismiss="alert" class="close" type="button">×</button>' +
        message +
        '</div>'
    );
    setAlertTimeOut(timeout);
}

var lang = document.documentElement.lang

if (lang == 'pt') {
    lang_code = 'pt-BR';
} else if (lang == 'en') {
    lang_code = 'en-US';
}

var summernoteConfig = {
    lang: lang_code,
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
        ['table', ['table']],
        ['insert', ['link', 'picture', 'video']],
        ['view', ['fullscreen', 'codeview', 'help']]
      ],
    placeholder: 'Escreva aqui o conteúdo desta publicação'
}

function selectorCallback(id, event) {
    url = window.location.origin + window.location.pathname + '?bra_id='+id;
    window.location = url;
}

function getParameterByName(name, url) {
    if (!url) url = window.location.href;
    url = url.toLowerCase();
    name = name.replace(/[\[\]]/g, "\\$&").toLowerCase();

    var regex = new RegExp("[?&]" + name + "(=([^&#]*)|&|#|$)"),
        results = regex.exec(url);
    if (!results) return null;
    if (!results[2]) return '';
    return decodeURIComponent(results[2].replace(/\+/g, " "));
}

function cropInput(crop, input, callback) {
    if (window.FileReader) {
        input.change(function() {
            var fileReader = new FileReader(),
                    files = this.files,
                    file;

            if (!files.length) {
                return;
            }

            file = files[0];

            if (/^image\/\w+$/.test(file.type) && file.size <= 5242880) {
                fileReader.readAsDataURL(file);
                fileReader.onload = function () {
                    input.val("");
                    crop.cropper("reset", true).cropper("replace", this.result);
                };

                if (callback !== null) {
                    callback();
                }

            } else {
                showMessage("Por favor escolha um arquivo de imagem, com no máximo 5 MB.");
            }
        });
    } else {
        input.addClass("hide");
    }
}
