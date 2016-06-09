$('.sidebar a').on('click', function(){
    $('.sidebar a').attr('class','');
    $(this).toggleClass('active');
});