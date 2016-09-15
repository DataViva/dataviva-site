var change_language = function(current_cnt, current_btn, hidden_cnt, hidden_btn, duration) {
	if (current_cnt.is(':visible')) {
		current_cnt.hide();
		current_btn.removeClass('active').attr('disabled', true);
		hidden_cnt.fadeToggle(duration);
		hidden_btn.addClass('active').attr('disabled', false);
	}
}

$(function() {
	if (dataviva.language == 'en' && $("[name='content-en']").length)
		$("[name='content-en']").fadeToggle()
	else
		$("[name='content-pt']").fadeToggle();

	var fade_duration = 800;

	$('#to-pt').on('click', function() {
		change_language(
			$("[name='content-en']"),
			$('#to-en'),
			$("[name='content-pt']"),
			$('#to-pt'),
			fade_duration
		);
	});

	$('#to-en').on('click', function() {
		change_language(
			$("[name='content-pt']"),
			$('#to-pt'),
			$("[name='content-en']"),
			$('#to-en'),
			fade_duration
		);
	});
});
