$(document).ready(function(){
    $('#birthday-date').datepicker({
        format: "dd/mm/yyyy",
        todayBtn: "linked",
        keyboardNavigation: false,
        forceParse: false,
        calendarWeeks: true,
        autoclose: true
    });
});

$(document).ready(function(){
    setAlertTimeOut(8000);
});