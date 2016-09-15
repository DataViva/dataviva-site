$(function() {
	if (dataviva.language == 'en' && $("[name='content-en']").length)
		$("[name='content-en']").fadeToggle()
	else
		$("[name='content-pt']").fadeToggle();

	$('#change-language').on('click', function() {
		var fade_duration = 800;
		if ($("[name='content-pt']").is(':visible')) {
			$("[name='content-pt']").hide();
			$("[name='content-en']").fadeToggle(fade_duration);
			$('#change-language').html('Ler em português');
		} else {
			$("[name='content-en']").hide();
			$("[name='content-pt']").fadeToggle(fade_duration);
			$('#change-language').html('Read in English');
		}
	});
});
