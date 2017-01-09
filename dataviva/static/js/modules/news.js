$(function() {
    $('#search-form').submit(function() {
        if ($(this).find('input').val())
            window.location.href = '/' + dataviva.language + '/news/?search=' + $(this).find('input').val().replace(' ', '+');
        else
            window.location.href = '/' + dataviva.language + '/news';
        return false;
    });
});
