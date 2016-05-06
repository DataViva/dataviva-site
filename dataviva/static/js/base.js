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
        "zeroRecords": dataviva.dictionary['zeroRecords'],
        "decimal": dataviva.language == "pt" ? "," : ".",
        "thousands": dataviva.language == "pt" ? "." : ","
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
  else return attr;
}

dataviva.getUrlAttr = function(attr) {
  if (attr == "Location") return 'bra';
  else if (attr == "Occupation") return 'cbo';
  else if (attr == "Industry") return 'cnae';
  else if (attr == "Product") return 'hs';
  else if (attr == "Trade_partner") return 'wld';
  else if (attr == "University") return 'university';
  else if (attr == "Major") return 'course_hedu';
  else if (attr == "Basic_course") return 'course_sc';
  else return attr;
}


var selectorHrefCallback = Selector()
    .callback(function(d){
        window.location = "/" + lang + "/" + dataviva.getAttrUrl(selectorHrefCallback.type()) + "/" + d.id +
        window.location.search;
    });

var select_attr = function(id) {
  d3.select("#modal-selector-content").call(selectorHrefCallback.type(id));
  $('#modal-selector').modal('show');
}

var selectorSearchCallback = Selector()
  .callback(function(d){
    window.location = window.location.pathname + "?" + selectorSearchCallback.type() + "_id="
    + d.id ;
  });

var select_attr_search = function(id) {
  d3.select("#modal-selector-content").call(selectorSearchCallback.type(id));
  $('#modal-selector').modal('show');
}

var drawProfileQuestionHeader = function() {
    var formattedChosenQuestion = chosenQuestion;
    $('#modal-search .chosen-options input').each(function(index, selector){
        if (selector.value != "") {
            var re = new RegExp(dataviva.dictionary[selector.id]+'\\s\\w', 'g'),
                questionOption = '<span class="question-option">'+dataviva[selector.id][selector.value].name+'</span>';
            formattedChosenQuestion = formattedChosenQuestion.replace(re, dataviva.dictionary[selector.id].toLowerCase()+' '+questionOption)
        }
    });

    var actualStep = $('#modal-search #actual-step').val();

    if ($.inArray(actualStep, ['entrepreneurs', 'development_agents', 'students']) > -1){
        $('#modal-search .current-question').html(dataviva.dictionary['select_search_question']);
    } else {
        $('#modal-search .current-question').html(dataviva.dictionary['select_search_'+actualStep]);
    }

    $('#modal-search .chosen-options #question').html(formattedChosenQuestion);
}

var profileSearchSelectorCallback = Selector()
    .callback(function(d){
        $('#modal-search-content .page-loader').remove();
        $('#modal-search .chosen-options #' + profileSearchSelectorCallback.type()).val(d.id);
        drawProfileQuestionHeader();
    });

var profile_search_selector = function(id) {
    $('#modal-search .modal-body').empty();

    drawProfileQuestionHeader();
    if ($.inArray(id, ['bra', 'cbo', 'cnae', 'hs', 'wld', 'university', 'course_hedu', 'course_sc' ]) > -1){
        d3.select("#modal-search-content").call(profileSearchSelectorCallback.type(id));
    } else {
        search(id);
    }

    $('#modal-search').modal('show');
}

var search = function(profile) {

    // Reset modal and set loading
    $('#modal-search .current-question').html(dataviva.dictionary['select_search_question']);
    $('#modal-search .modal-body').empty();
    $('#modal-search .chosen-options #question').empty();
    $('#modal-search #profile').val(profile);
    $('#modal-search #actual-step').val(profile);
    $('#modal-search #answer').val('');

    $('#modal-search #search-advance').prop("disabled", true);
    $('#modal-search #search-back').hide();

    var search_load = new dataviva.ui.loading($('#modal-search .modal-body').get(0));
    search_load.text(dataviva.dictionary['loading']);

    $('#modal-search').modal('show');

    dataviva.requireAttrs(['bra', 'cbo', 'cnae', 'hs'], function() {
        $.ajax({
          method: "GET",
          url: "/" + lang + "/search/profile/" + profile,
          success: function (response) {
            search_load.hide();

            var questions = response.questions;
            // Set modal template
            $('#modal-search .modal-search-title').html(response.profile);
            $('#modal-search .modal-body').html(response.template);

            for (id in questions) {

                var question = questions[id],
                    selectors = questions[id].selectors,
                    div = $('<div></div>').addClass('selector-list-item');

                // Append questions
                div.append('<div></div>')
                        .addClass('item-title')
                        .html(question.description)
                        .attr('id', 'question'+id)
                        .data('answer', question.answer)
                        .data('selectors', selectors.join(','));

                // Choose Question
                div.click(function() {
                    $('#modal-search #search-advance').prop('disabled', false);
                    $(this).siblings('.selected').toggleClass('selected');
                    $(this).toggleClass('selected');

                    window.chosenQuestion = $(this).html();

                    $('#modal-search .chosen-options #question').html($(this).html());
                    $('#modal-search .chosen-options input').remove()
                    $('#modal-search #answer').val($(this).data('answer'));

                    var selectors = $(this).data('selectors').split(',');

                    for (var i = 0; i < selectors.length; i++) {
                        var selector = selectors[i];
                            selectorInput = $('<input>')
                                .attr('type', 'hidden')
                                .attr('id', selector);
                            $('#modal-search .chosen-options').append(selectorInput);
                    }
                });

                $('#modal-search .selector-list .list-group').append(div);
            }
          }
        });
    });
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

    $('a[data-search]').click(function() {
        search($(this).data('search'));
    });

    $("#modal-selector").on('hidden.bs.modal', function () {
      $(this).find('.modal-body').empty();
    })
    $("#modal-search").on('hidden.bs.modal', function () {
      $(this).find('.modal-body').empty();
    })

    $('#modal-search #search-advance').click(function() {
        var answer = $('#modal-search #answer').val();
        $('#modal-search #search-back').show();

        $('#modal-search .chosen-options input').each(function(index, el) {
            if (this.value == "") {
                $('#modal-search #actual-step').val(this.id);
                profile_search_selector(this.id);
                return false;
            }
        });

        if ($.inArray("", $('#modal-search .chosen-options input').map(function(){return this.value;}).get()) == -1) {
            window.location = '/' + lang + answer.format.apply(
                answer,
                $('#modal-search .chosen-options input').map(function(){return this.value;}).get()
            );
        }
    });

    $('#modal-search #search-back').click(function() {
        var actualStep = $('#modal-search #actual-step');
        var actualInput = $('#modal-search .chosen-options #'+actualStep.val());

        var previousSelector = actualInput.prev().get(0).id;
        if ($.inArray(previousSelector, ['bra', 'cbo', 'cnae', 'hs', 'wld', 'university', 'course_hedu', 'course_sc' ]) > -1){
            actualInput.val('');
            actualStep.val(previousSelector);
            profile_search_selector(previousSelector);
        } else {
            search($('#modal-search #profile').val());
        }
    });

    $('.btn-toggle').click( function() {
        $(this).toggleClass('selected');
        return false
    });
});

