var NewSelector = (function(){
	var searchInputTemplate = 
	'<div class="selector">' +
	    '<div class="selector_header">' +
	        '<div class="leon text">' +
	            '<input type="text" class="form-control" id="cnae_search" placeholder="PESQUISE">' +
	        '</div>' +
	    '</div>' +
	    '<div class="selector_body">' +
	    '</div>' +
	'</div>';

	var itemTemplate = '' + 
	'<div class="search_result">' +
	    '<div class="icon-box"><i class="search_icon dv-course-sc-xx" style="color: rgb(47, 47, 109);"></i></div>' +
	    '<div class="search_text">' +
	        '<div class="search_title" style="color: rgb(47, 47, 109);">{{name}}</div>' +
	        '<div class="search_data">CNES ID: {{cnes_id}}</div>' +
	    '</div>' +
	    '<div class="search_buttons">' +
	        '<a href="/pt/health/{{cnes_id}}" class="m-l-xs btn btn-primary btn-outline btn-toggle"><i class="fa fa-check-square-o"></i>Selecione</button>' +
	    '</div>' +
	'</div>' +
	'<div class="d3plus_tooltip_data_seperator"></div>'

	var show = function(){
		$('#modal-selector').modal('show');
		var loading = dataviva.ui.loading('#modal-selector-content').text('Carregando');
		$.ajax({
		    url: 'http://api.staging.dataviva.info/metadata/state',
		    type: 'GET',
		    success: function(response){
		    	loading.hide();
		    	$('#modal-selector .modal-header h4.modal-title').html('Estabelecimentos')
		    	$('#modal-selector-content').append($(searchInputTemplate))
		    	for(var key in response){
		    		$('#modal-selector-content .selector_body').append($(itemTemplate.replace('{{name}}', response[key].name_pt).replace('{{cnes_id}}', key)))
		    	}

		    	addFilter()
		    }
		});
	};

	var addFilter = function(){
		$('#cnae_search').on('keyup', function(el){
			var query = el.target.value.toLowerCase();
			
			document.querySelectorAll('#modal-selector-content .search_title').forEach(function(item){
				var itemHealth = item.innerHTML.toLowerCase();
				if(itemHealth.indexOf(query) == -1)
					item.closest('.search_result').style.display = 'None'
				else
					item.closest('.search_result').style.display = 'block'
			});
		})
	};

	return {
		show: show
	}
})();

