$(function() {
    $('#search-form').submit(function() {
        window.location.href = '/' + dataviva.language + '/news/?search=' + $(this).find('input').val().replace(' ', '+');
        return false;
    });
});
