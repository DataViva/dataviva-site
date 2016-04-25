dataviva.load = function(name, url, callBack) {
    var parseAttr = function(data) {
        var attr = {};
        for (var i = 0; i < data.length; ++i) {
            attr[data[i].id] = data[i];
        }

        return attr;
    }

    var requestData = function(loadData) {
        $.ajax({
            dataType: 'json',
            method: 'GET',
            url: url,
            success: function (response) {
                localforage.setItem(url, response, loadData);
            }
        });
    }

    var loadData = function() {
        localforage.getItem(url, function(err, attr) {
            if(attr) {
                window.dataviva[name] = parseAttr(attr.data);
                if (callBack) {
                    callBack(name);
                }
            } else {
                requestData(loadData);
            }
        });
    }

    loadData();
}

dataviva.requireAttrs = function(attrs, callBack) {
    var queue = attrs;

    var ready = function(attr) {
        queue.splice(queue.indexOf(attr), 1);

        if (queue.length == 0) {
            callBack();
        }
    }

    attrs.forEach(function(attr) {
        dataviva.load(attr, '/attrs/'+attr+'/?lang='+lang, ready);
    });
}

dataviva.datatables = {
    language: {
        "loading": dataviva.dictionary['loading'] + "...",
        "emptyTable": dataviva.dictionary['emptyTable'],
        "info": dataviva.dictionary['infoResults'],
        "infoEmpty": dataviva.dictionary['infoEmpty'],
        "infoFiltered": dataviva.dictionary['infoFiltered'],
        "processing": dataviva.dictionary['processing'] + "...",
        "search": dataviva.dictionary['dataTableSearch'] + ":",
        "zeroRecords": dataviva.dictionary['zeroRecords']
    }
}


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
    if (timeout) {
        setAlertTimeOut(timeout);
    }
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

// Create Filter Selector
dataviva.popover.create({
  "id": "filter_popover",
  "width": 600,
  "height": "80%",
  "close": true
})

dataviva.getAttrUrl = function(attr) {
  if (attr == "bra") return 'location';
  else if (attr == "cbo") return 'occupation';
  else if (attr == "cnae") return 'industry';
  else if (attr == "hs") return 'product';
  else if (attr == "wld") return 'trade_partner';
  else if (attr == "university") return 'university';
  else if (attr == "course_hedu") return 'major';
  else if (attr == "course_sc") return 'basic_course';
  else return '';
}

var selector = Selector()
  .callback(function(d){
    window.location = "/" + lang + "/" + dataviva.getAttrUrl(selector.type()) + "/" + d.id;
  });

function select_attr(id) {
  d3.select("#modal-selector-content").call(selector.type(id));
  $('#modal-selector').modal('show');
}

d3.selectAll(".profile_simple").on("click", function(){
  // stop from bubbling up so selector isn't triggered
  d3.event.stopPropagation();
})

$(document).ready(function () {
    new WOW().init();
    $("[data-toggle=popover]").popover({ trigger: "hover" });
    $('.counter').counterUp();
    $.stellar();

    $( ".js-switch" ).each(function() {
        var switchery = new Switchery(this, {
            color: '#5A9DC4'
        });
    });

    (function(d, s, id) {
        var js, fjs = d.getElementsByTagName(s)[0];
        if (d.getElementById(id)) return;
        js = d.createElement(s); js.id = id;
        js.src = "//connect.facebook.net/pt_BR/sdk.js#xfbml=1&version=v2.5&appId=222520191136295";
        fjs.parentNode.insertBefore(js, fjs);
    }(document, 'script', 'facebook-jssdk'));


    $("[name='language-selector']").val(document.documentElement.lang);

    $("[name='language-selector']").change(function() {
        var path = window.location.pathname.split('/'),
            lang = path[1];

        if (lang !== this.value) {
            if (['pt','en'].indexOf(lang) > -1) {
                path.splice(1, 1, this.value);
            } else {
                path.splice(1, 0, this.value);
            }
            window.location.href = path.join('/') + window.location.search + window.location.hash;
        }
    });
});

