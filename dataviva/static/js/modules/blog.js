$(function() {
    $('#search-form').submit(function() {
        window.location.href = '/' + dataviva.language + '/blog/?search=' + $(this).find('input').val().replace(' ', '+');
        return false;
    });
});
