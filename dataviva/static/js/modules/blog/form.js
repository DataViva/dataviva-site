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

var add_caption = function(image) {
    image.wrap('<figure> </figure>');
    figcaption = $('<figcaption> </figcaption>');
    if (image.attr('data-original-title'))
        figcaption.html(image.attr('data-original-title'));
    figcaption.appendTo(image.parent());
    var image_float = image.css('float');
    var image_width = image.css('width');
    if (image_float == 'left' || image_float == 'right') {
        image
            .css('float', 'none')
            .parent().css('float', image_float);
    }
    image.parent().css('width', image_width);
    image.css('width', '100%');
}

var remove_caption = function(image) {
    image.siblings('figcaption').remove();
    var figure_width = image.parent().css('width');
    image.css('width', figure_width);
    var figure_float = image.parent().css('float');
    if (figure_float == 'left' || figure_float == 'right')
        image.css('float', figure_float);
    image.unwrap();
}

var load_tooltips = function() {
    $('[data-toggle="tooltip"]').each(function() {
        var image_title = $(this).attr('title');
        $(this).attr('title', '');
        $(this).tooltip();
        $(this).attr('title', image_title);
    });
}

var show_editor = function(edit_button, preview_button, editor) {
    preview_button.prop('disabled', false);
    edit_button.prop('disabled', true);
    summernoteConfig['focus'] = true;
    editor.find('img').each(function() {
        if ($(this).parent().is('figure'))
            remove_caption($(this));
    });
    editor.summernote(summernoteConfig);
    load_tooltips();
}

var show_preview = function(edit_button, preview_button, editor, text_content) {
    preview_button.prop('disabled', true);
    edit_button.prop('disabled', false);
    editor.summernote('destroy');
    editor.find('img').each(function() {
        add_caption($(this));
    });
    var aHTML = editor.html();
    text_content.val(aHTML);
}

$(document).ready(function(){

    $('#blog-edit-pt, #blog-edit-en').prop('disabled', true);

    $('#text-content-editor-pt').append($('#text_content').val());
    $('#text-content-editor-en').append($('#text_content_en').val());

    $('#text-content-editor-pt img, #text-content-editor-en img').each(function() {
        if ($(this).parent().is('figure'))
                remove_caption($(this));
    });

    $('#text-content-editor-pt').summernote(summernoteConfig);
    $('#text-content-editor-en').summernote(summernoteConfig);

    $('#blog-edit-pt').click(function() {
        show_editor(
            $('#blog-edit-pt'),
            $('#blog-preview-pt'),
            $('#text-content-editor-pt')
        );
    });
    $('#blog-edit-en').click(function() {
        show_editor(
            $('#blog-edit-en'),
            $('#blog-preview-en'),
            $('#text-content-editor-en')
        );
    });

    $('#blog-preview-pt').click(function() {
        show_preview(
            $('#blog-edit-pt'),
            $('#blog-preview-pt'),
            $('#text-content-editor-pt'),
            $('text_content')
        );
    });
    $('#blog-preview-en').click(function() {
        show_preview(
            $('#blog-edit-en'),
            $('#blog-preview-en'),
            $('#text-content-editor-en'),
            $('text_content_en')
        );
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
    $('#textarea-feedback').html(text_max + ' ' + dataviva.dictionary['characters_left']);

    $('#text_call').keyup(function() {
        var text_length = $('#text_call').val().length;
        var text_remaining = text_max - text_length;

        $('#textarea-feedback').html(text_remaining + ' ' + dataviva.dictionary['characters_left']);
    });

    load_tooltips();

    $('#blog-form').submit(function() {
        $('#blog-form > button[type=submit]').prop('disabled', true);
        $('#summernote-pt').hide();
        $('#summernote-en').hide();

        var submittingForm = dataviva.ui.loading('#blog-form');
        submittingForm.text(dataviva.dictionary['loading'] + "...");

        $('#text-content-editor-pt').summernote('destroy');
        $('#text-content-editor-en').summernote('destroy');

        $('#text-content-editor-pt img, #text-content-editor-en img').each(function() {
            if ($(this).parent().is('figure') == false)
               add_caption($(this));
        });

        var pt_html = $('#text-content-editor-pt').html();
        $('#text_content').val(pt_html);
        if ($('#text-content-editor-pt').summernote('isEmpty')) {
            $('#text_content').val('');
        }

        var en_html = $('#text-content-editor-en').html();
        $('#text_content_en').val(en_html);
        if ($('#text-content-editor-en').summernote('isEmpty')) {
            $('#text_content_en').val('');
        }

        return true;
    });
});
