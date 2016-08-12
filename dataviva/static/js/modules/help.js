$('.sidebar a').on('click', function(){
    $('.sidebar a').attr('class','');
    $(this).toggleClass('active');
});


$("#home .col-md-6 > .panel-heading > h2 a").on('click', function(){
    $('.sidebar a').attr('class','');
    $('#sidebar_' + $(this).parent().parent()[0].id).toggleClass('active');
});