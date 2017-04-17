var lang = location.pathname.split('/')[1];
var dictionary = {};
var establishments_xhr;

dictionary['establishments'] = lang == 'en' ? 'Establishments' : 'Estabelecimentos';
dictionary['select'] = lang == 'en' ? 'Select' : 'Selecione';
dictionary['search-input-placeholder'] = lang == 'en' ? 'SEARCH' : 'PESQUISE';
dictionary['search-input-helper'] = lang == 'en' ? 'Press ENTER to search' : 'Aperte ENTER para pesquisar';
dictionary['no-data-clusterize'] = lang == 'en' ? 'No data found' : 'Nenhum registro encontrado';
dictionary['search-input-description'] = lang == 'en' ? 'Find an establishment by ID, name or location.' : 'Procure um estabelecimento pelo ID, nome ou localidade.';

var EstablishmentSelector = (function(){
	
	var data = {};
	var items = [];
	var clusterize;

	var Template = (function(){

		var searchWidget = '' +
		'<div class="leon text">' +
		    '<input type="text" class="form-control" id="search-input" placeholder=" ' + dictionary['search-input-placeholder'] + '">' +
		'</div>' +
		'<div class="leon text" id="search-helper" style="display: none; padding-left: 15px; padding-top: 5px">' +
		    '<small>' + dictionary['search-input-helper'] + '</small>' +
		'</div>';
		

		var establishmentWidget = '' + 
		'<div class="search_result" >' +
			'<div class="icon-box"><i class="search_icon dv-university-t" style="color: rgb(158, 218, 229);"></i></div>' +
		    '<div class="search_text">' +
		        '<div class="search_title" style="color: rgb(47, 47, 109);">{{name}}</div>' +
		        '<div class="search_data">ID: {{id}}</div>' +
		        '<div class="search_data">{{municipality}}</div>' +
		    '</div>' +
		    '<a href="/' + lang + '/health/{{id}}" class="m-l-xs btn btn-primary btn-outline btn-toggle" style="position: absolute; right: 15px; top: 13px;">' + 
		        dictionary['select'] + 
		    '</a>' + 
		'</div>' +
		'<div class="d3plus_tooltip_data_seperator"></div>';


		var selectorTemplate = '' + 
		'<div class="selector">' +
			'<div class="selector_header"></div>' +
			'<div class="selector_body" id="contentArea">' +
				'<div class="search_error">' + dictionary['search-input-description'] + '</div class="search_error">' +
			'</div>' +
		'</div>';

		return {
			searchWidget: searchWidget,
			establishmentWidget: establishmentWidget,
			selectorTemplate: selectorTemplate
		};
	})();

	var Modal = (function(){
		var buildModal = function(){
			$('#modal-selector .modal-header h4.modal-title').html(dictionary['establishments'])
			$('#modal-selector-content').empty();
			$('#modal-selector-content').append($(Template.selectorTemplate));
			$('#modal-selector-content .selector_header').append($(Template.searchWidget));
		};

		var show = function(){
			buildModal();
			$('#modal-selector').modal('show');
			var loading = dataviva.ui.loading('#modal-selector-content').text('Carregando');

			clusterize = new Clusterize({
				scrollId: 'contentArea',
				contentId: 'contentArea',
				no_data_text: dictionary['no-data-clusterize']
			});

			loading.hide();

			$("#search-input").keyup(function(ev){
				var query = ev.target.value;

				if(query.length > 1)
					$('#search-helper').show();
				else{
					$('#search-helper').hide();
					return;
				}

				if(ev.which != 13)
					return;

				if(establishments_xhr)
					establishments_xhr.abort();

				get(query);
			})

		};

		var render = function(){
			var itemsToString = function(){
				var list = [];

				items.forEach(function(x){
					var item = Template.establishmentWidget
						.replace(/{{name}}/g, x.name)
						.replace(/{{id}}/g, x.id)
						.replace(/{{municipality}}/g, x.municipality)

					list.push(item)
				})

				return list;
			};

			clusterize.update(itemsToString());
			clusterize.refresh();
		}

		var get = function(query){
			var loading = dataviva.ui.loading('#modal-selector-content').text('Carregando');

			establishments_xhr = $.ajax({
				url: 'http://api.staging.dataviva.info/search/cnes',
				data: {
					query: query
				},
				success: function(result){
					items = result.data;
					render();
					$('#search-helper').hide();
					loading.hide();
				}
			})
		}

		return {
			show: show,
			render: render,
			get: get
		};
	})();

	return {
		show: Modal.show,
		get: Modal.get
	}
})();