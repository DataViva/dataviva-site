$('#help-center').click(function(){
	  $('.tab-content #home').addClass('active').siblings().removeClass('active');
});

$('.sidebar ul li a').click(function(){
	$('.sidebar ul li a').removeClass('active');
	$(this).addClass('active');
});