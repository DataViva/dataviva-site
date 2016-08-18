var Publication = function() {
    var self = this;

    self.status = false;

    self.submit_form = function(result) {
        file_paths = result.file_paths;
        for (var i = 0; i < file_paths.length; i++) {
            $('#text-content-editor img[name=img' + file_paths[i]['id'] + ']')
                .attr('src', file_paths[i]['path'])
                .removeAttr('data-filename')
                .removeAttr('name');
        }
        $('figure').each(function() {
            if ($(this).children('img').length == 0) {
                $(this).children('figcaption').remove();
            }
        })
        text_content = $('#text-content-editor').html();
        $('#text_content').val(text_content);
        self.status = true;
        $('#news-form').submit();
    }

}

var inputThumbCallback = function() {
    $('#thumb-img').hide();
    $('.thumb-buttons').hide();

    $('#thumb-preview').show();
    $('.crop-buttons').show();
    $('.thumb-crop').show();

    $($('#thumb-crop')).cropper({
        aspectRatio: 350/227,
        preview: '#thumb-preview',
        viewMode: 3
    });
}

function add_caption(image) {
    var title = '';
    if (typeof image.attr('title') !== 'undefined')
        title = image.attr('title');
    if (image.parent().is('figure')) {
        if (image.parent().find('figcaption').length == 0)
            $('<figcaption><i>' + title + '</i></figcaption>').appendTo(image.parent());
        else
            image.parent().find('figcaption i').html(title);
    } else {
        image.wrap('<figure> </figure>');
        $('<figcaption><i>' + title + '</i></figcaption>').appendTo(image.parent());
        image.parent()
            .wrap('<p> </p>')
            .attr('contenteditable', 'false');
    }   
}

$(document).ready(function(){
    var publication = new Publication();

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

    cropInput($('#thumb-crop'), $('#thumb-input'), inputThumbCallback)

    $('#thumb-zoomIn').click(function() {
        $('#thumb-crop').cropper('zoom', 0.1);
    });
    $('#thumb-zoomOut').click(function() {
        $('#thumb-crop').cropper('zoom', -0.1);
    });
    $('#thumb-rotateLeft').click(function() {
        $('#thumb-crop').cropper('rotate', 45);
    });
    $('#thumb-rotateRight').click(function() {
        $('#thumb-crop').cropper('rotate', -45);
    });
    $('#thumb-save').click(function() {
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


    $('#publish-date').datepicker({
        format: "dd/mm/yyyy",
        todayBtn: "linked",
        keyboardNavigation: false,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });

    var text_max = 500;
    $('#textarea-feedback').html(text_max + ' caracteres restantes');

    $('#text_call').keyup(function() {
        var text_length = $('#text_call').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback').html(text_remaining + ' caracteres restantes');
    });

    var submittingForm = dataviva.ui.loading('#news-form');
    submittingForm.text(dataviva.dictionary['loading'] + "...");
    submittingForm.hide();

    $('#news-form').submit(function() {
        if (publication.status) {
            return publication.status;
        } else {
            submittingForm.show();
            $('#text-content-editor').summernote('destroy');
            $('#text-content-editor').hide();
            $('button[type=submit]').prop('disabled', true);
            var data = new FormData();
            $('#text-content-editor img').each(function(i) {
                data.append(i+1, $(this).attr('src'));
                $(this).attr('name', 'img' + (i+1));
            });
            data.append('csrf_token', $('#csrf_token').val());
            $.ajax({
                url: '/' + dataviva.language + '/news/admin/publication/new/upload',
                cache: false,
                contentType: false,
                processData: false,
                data: data,
                type: 'POST',
                success: function (result) {
                    publication.submit_form(result);
                }
            });
            return false;
        }
    });
});
