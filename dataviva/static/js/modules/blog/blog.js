$(function() {
	dataviva.language == 'en' && $("[name='content-en']").length ? $("[name='content-en']").show() : $("[name='content-pt']").show();

	$('#change-language').on('click', function() {
		if ($("[name='content-en']").length) {
			if ($("[name='content-pt']").is(':visible')) {
				$("[name='content-pt']").hide();
				$("[name='content-en']").show();
				$('#change-language').html('Ler em português');
			} else {
				$("[name='content-en']").hide();
				$("[name='content-pt']").show();
				$('#change-language').html('Read in English');
			}
		}
	});

});

