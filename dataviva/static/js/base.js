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