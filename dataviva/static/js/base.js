localforage.getItem("version", function(error, version){
  if (error || version !== dataviva.attr_version) {
    localforage.clear(function(){
      localforage.setItem("version", dataviva.attr_version);
    })
  }
});

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
        ['insert', ['link', 'picture', 'chart', 'video']],
        ['view', ['fullscreen', 'codeview', 'help']]
      ],
    popover: {
        image: [
            ['imagesize', ['imageSize100', 'imageSize50', 'imageSize25']],
            ['float', ['floatLeft', 'floatRight', 'floatNone']],
            ['remove', ['removeMedia']],
            ['custom', ['imageTitle']]
        ]
    },
    placeholder: dataviva.dictionary['summernote_placeholder'],
    imageTitle: {
        specificAltField: true,
    },
    callbacks: {
        onImageUpload: function(files) {
            var summernoteLoading = dataviva.ui.loading('#summernote');
            summernoteLoading.text(dataviva.dictionary['loading'] + "...");
            var file = files[0],
                data = new FormData();
            data.append('image', file);
            data.append('csrf_token', $('#csrf_token').val());
            $.ajax({
                type: 'POST',
                url: '/' + dataviva.language + '/' + window.location.pathname.split('/')[2] + '/admin/upload',
                cache: false,
                contentType: false,
                processData: false,
                data: data,
                success: function(data) {
                    $('#text-content-editor').summernote('insertImage', data.image.url);
                },
                error: function(err) {
                    swal({
                        title: 'Ops!',
                        text: dataviva.dictionary['file_too_large'],
                        type: "error"
                    });
                },
                complete: function() {
                    summernoteLoading.hide();
                }
            });
        }
    }
}

var select2Config = {
    tags: true,
    tokenSeparators: [',']
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

dataviva.getArgUrl = function(arg){
    var params = window.location.href.split('?')[1];

    if(params){
        params = params.split(/=|&/);
        var argIndex = params.indexOf(arg);

        if(argIndex != -1)
            return params[argIndex + 1];
        else
            return null;
    }
}

var selectorHrefCallback = Selector()
    .callback(function(d){
        var argBra = dataviva.getArgUrl('bra_id');
        window.location = "/" + lang + "/" + dataviva.getAttrUrl(selectorHrefCallback.type()) + "/" + d.id  + 
                            ((argBra) ? '?bra_id=' +  argBra : '' );
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
            var re = new RegExp(dataviva.dictionary[selector.id]+'\\s\\w', 'g');

            if (selector.value == 'all') {
                var questionOption = '<span class="question-option">'+dataviva.dictionary['brazil']+'</span>';
            } else {
                var questionOption = '<span class="question-option">'+dataviva[selector.id][selector.value].name+'</span>';
            }

            formattedChosenQuestion = formattedChosenQuestion.replace(re, dataviva.dictionary[selector.id].toLowerCase()+' '+questionOption)
        }
    });

    var actualStep = $('#modal-search #actual-step').val();

    if ($.inArray(actualStep, ['entrepreneurs', 'development_agents', 'students']) > -1){
        $('#modal-search #current-question').html(dataviva.dictionary['select_search_question']);
    } else {
        $('#modal-search #current-question').html(dataviva.dictionary['select_search_'+actualStep]);
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
    $('#modal-search #actual-step').val(id);
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
    $('#modal-search #current-question').html(dataviva.dictionary['select_search_question']);
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
            window.location.href = path.join('/') + window.location.search.replace('subject=' + dataviva.getArgUrl('subject'), '') + window.location.hash;
        }
    });

    $('a[data-search]').click(function() {
        search($(this).data('search'));
    });

    $("#modal-selector").on('hidden.bs.modal', function () {
      $(this).find('.modal-body').empty();
    });
    $("#modal-search").on('hidden.bs.modal', function () {
      $(this).find('.modal-body').empty();
    });
    $("#modal-dataviva-video").on('hidden.bs.modal', function () {
      $(this).find('.video-wrapper').empty();
    });

    $('#modal-search #search-advance').click(function() {
        var answer = $('#modal-search #answer').val();
        $('#modal-search #search-back').show();
        if ($('#modal-search .chosen-options #'+$('#modal-search #actual-step').val()).val() == '') {
            $('#current-question').addClass('animated');
            $('#current-question').addClass('tada');
            setTimeout(function(){$('#current-question').removeAttr('class').attr('class', '');}, 1000);
        } else {
            $('#modal-search .chosen-options input').each(function(index, el) {
                if (this.value == "") {
                    profile_search_selector(this.id);
                    return false;
                }
            });
        }

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

    $('.embed-video-link').click(function() {
        $('#modal-dataviva-video .video-wrapper').html('<iframe class"embed-responsive-item" src="' + this.href +
                                                         '" frameborder="0" allowfullscreen></iframe>');
        $('#modal-dataviva-video').modal('show');
        return false; // cancel the event
    });

    (function($) {

      'use strict';

      var AjaxForms = {

        // Initialization the functions
        init: function() {
          AjaxForms.SignUp();
          AjaxForms.Login();
          AjaxForms.Contact();
        },

        removeWarnings: function(input) {
            var $input = $(input);

            if ($input.hasClass('error')) {
                $input.closest('.form-group').removeClass('has-error');
                $input.siblings().remove('label.error');
                $input.removeClass('error');
            }

            if ($input.hasClass('success')) {
                $input.closest('.form-group').removeClass('has-success');
                $input.removeClass('success');
            }
        },

        // SignUp Form
        SignUp: function() {
          // Checking form input when focus and keypress event
          $('#modal-signup-form input[type="text"], #modal-signup-form input[type="email"], #modal-signup-form input[type="checkbox"], #modal-signup-form input[type="password"], #modal-signup-form select')
                .on('focus keypress', function() {
                    AjaxForms.removeWarnings(this);
                });

          // Signup form when submit button clicked
          $('#modal-signup-form').submit(function() {
            var $form         = $(this);
            var submitData    = $form.serialize();
            var $fullname     = $form.find('input[name="fullname"]');
            var $email        = $form.find('input[name="email"]');
            var $submit       = $form.find('input[name="submit"]');
            var $password     = $form.find('input[name="password"]');
            var $confirm      = $form.find('input[name="confirm"]');
            var $agree_mailer = $form.find('input[name="agree_mailer"]');
            var status        = true;

            if ($fullname.val() === '') {
                $fullname.closest('.form-group').addClass('has-error');
                $fullname.addClass('error');
                status = false;
            }

            if ($email.val() === '') {
                $email.closest('.form-group').addClass('has-error');
                $email.addClass('error');
                status = false;
            }

            if ($password.val() === '') {
                $password.closest('.form-group').addClass('has-error');
                $password.addClass('error');
                status = false;
            }

            if ($confirm.val() === '') {
                $confirm.closest('.form-group').addClass('has-error');
                $confirm.addClass('error');
                status = false;
            }

            if (status) {
              $fullname.attr('disabled', 'disabled');
              $email.attr('disabled', 'disabled');
              $submit.attr('disabled', 'disabled');
              $("[name='submit']").attr('disabled', 'disabled');

              $.ajax({
                type: 'POST',
                url: '/' + dataviva.language + '/user/new',
                data: submitData,
                dataType: 'html',
                success: function(response) {
                    $('#dataviva-signup').modal('hide');
                    swal({
                        title: dataviva.dictionary['thank_you'] + '!',
                        text: response,
                        type: "success"
                    });
                },
                error: function(response) {
                    var IS_JSON = true;
                        try {
                            var errors = $.parseJSON(response.responseText);
                            for (var field in errors) {
                                AjaxForms.removeWarnings($form.find('#'+field));
                                $form.find('#'+field).addClass('error');
                                $form.find('#'+field).closest('.form-group').addClass('has-error');

                                var error = $('<label></label>').attr('class', 'm-l-md error').html(errors[field]);
                                $form.find('#'+field).siblings('.control-label').after(error);
                            }
                        }
                        catch(err) {
                            swal({
                                title: 'Ops!',
                                text: response.responseText,
                                type: "error"
                            });
                        }
                }
              }).always(function() {
                    $fullname.prop('disabled', false);
                    $email.prop('disabled', false);
                    $submit.prop('disabled', false);
                    $("[name='submit']").prop('disabled', false);
              });
            }

            status = true;

            return false;
          });
        },

        // Contact Form
        Contact: function() {
          var pattern = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i;



            // Checking form input when focus and keypress event
            $('#contact-form input[type="text"], #contact-form input[type="email"], #contact-form textarea, #contact-form select')
                .on('focus keypress', function() {
                    AjaxForms.removeWarnings(this);
                });


            // Signup form when submit button clicked
            $('#contact-form').submit(function() {
                var $form       = $(this);
                var submitData  = $form.serialize();
                var $name       = $form.find('input[name="name"]');
                var $email      = $form.find('input[name="email"]');
                var $message    = $form.find('textarea[name="message"]');
                var $submit     = $form.find('input[name="submit"]');
                var status      = true;
                if ($name.val() === '') {
                    $name.closest('.form-group').addClass('has-error');
                    $name.addClass('error');
                    status = false;
                }
                if ($email.val() === '' || pattern.test($email.val()) === false) {
                    $email.closest('.form-group').addClass('has-error');
                    $email.addClass('error');
                    status = false;
                }
                if ($message.val() === '') {
                    $message.closest('.form-group').addClass('has-error');
                    $message.addClass('error');
                    status = false;
                }

                if (status) {
                    $name.attr('disabled', 'disabled');
                    $email.attr('disabled', 'disabled');
                    $message.attr('disabled', 'disabled');
                    $submit.attr('disabled', 'disabled');

                    $.ajax({
                        type: 'POST',
                        url: '/' + dataviva.language + '/contact/',
                        data: submitData,
                        dataType: 'html',
                        success: function(response) {
                            swal({
                                title: dataviva.dictionary['thank_you'] + '!',
                                text: response.message,
                                type: "success"
                            });
                            $name.prop('disabled', false);
                            $email.prop('disabled', false);
                            $message.prop('disabled', false);
                            $submit.prop('disabled', false);
                        },
                        error: function(response) {
                            var errors = $.parseJSON(response.responseText);
                            for (var field in errors) {
                                AjaxForms.removeWarnings($form.find('#'+field));
                                $form.find('#'+field).addClass('error');
                                $form.find('#'+field).closest('.form-group').addClass('has-error');

                                var error = $('<label></label>').attr('class', 'm-l-md error').html(errors[field]);
                                $form.find('#'+field).siblings('.control-label').after(error);
                            }
                        }
                    });
                }

                status = true;

                return false;
            });
        },

        // Login Form
        Login: function() {
          //var pattern = /^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))$/i;

          // Checking form input when focus and keypress event
          $('#dataviva-login-form input[type="text"], #dataviva-login-form input[type="email"], #dataviva-login-form input[type="checkbox"], #dataviva-login-form input[type="password"], #dataviva-login-form select')
                .on('focus keypress', function() {
                    AjaxForms.removeWarnings(this);
                });

          // Signup form when submit button clicked
          $('#dataviva-login-form').submit(function() {
            var $form         = $(this);
            var submitData    = $form.serialize();
            var $email        = $form.find('input[name="email"]');
            var $password     = $form.find('input[name="password"]');
            var $submit       = $form.find('input[name="submit"]');
            var status        = true;

            if ($email.val() === '' ) {
                $email.closest('.form-group').addClass('has-error');
                $email.addClass('error');
                status = false;
            }

            if ($password.val() === '' ) {
                $password.closest('.form-group').addClass('has-error');
                $password.addClass('error');
                status = false;
            }

            if (status) {
              $password.attr('disabled', 'disabled');
              $email.attr('disabled', 'disabled');
              $submit.attr('disabled', 'disabled');

              $.ajax({
                type: 'POST',
                url: '/' + dataviva.language + '/session/login',
                data: submitData,
                dataType: 'html',
                success: function(response) {
                    $('#dataviva-signup').modal('hide');
                    location.reload();
                },
                error: function(response) {
                    var IS_JSON = true;
                        try {
                            var errors = $.parseJSON(response.responseText);
                            for (var field in errors) {
                                AjaxForms.removeWarnings($form.find('#'+field));
                                $form.find('#'+field).addClass('error');
                                $form.find('#'+field).closest('.form-group').addClass('has-error');

                                var error = $('<label></label>').attr('class', 'm-l-md error').html(errors[field]);
                                $form.find('#'+field).siblings('.control-label').after(error);
                            }
                        }
                        catch(err) {
                            swal({
                                title: 'Ops!',
                                text: response.responseText,
                                type: "error"
                            },
                            function(isConfirm){
                                if (response.status == 401){
                                    window.location.pathname = "/" + dataviva.language + "/user/confirm_pending/" + $form.find('input[name="email"]').val()
                                }
                            });
                        }
                }
                }).always(function() {
                    $password.prop('disabled', false);
                    $email.prop('disabled', false);
                    $submit.prop('disabled', false);
                });
            }

            status = true;

            return false;
          });
        }
      };

      // Run the main function
      $(function() {
        AjaxForms.init();
      });

    })(window.jQuery);
});

$(document).ready(function() {
    $('[data-toggle=offcanvas]').click(function() {
        $('.row-offcanvas').toggleClass('active');
    });
});