$(function() {
    $('#search-form').submit(function() {
        if ($(this).find('input').val())
            window.location.href = '/' + dataviva.language + '/blog/?search=' + $(this).find('input').val().replace(' ', '+');
        else
            window.location.href = '/' + dataviva.language + '/blog';
        return false;
    });
});
