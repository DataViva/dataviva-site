$(document).ready(function () {
    new WOW().init();
    $("[data-toggle=popover]").popover({ trigger: "hover" });
    $('.counter').counterUp();
    $.stellar();
});

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
