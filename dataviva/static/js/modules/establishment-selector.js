var EstablishmentSelector = (function(){
	
	var data = {};
	var items = [];
	var clusterize;

	var Template = (function(){
		var filterWidget  = '' +
		'<div class="selector_header_icon" style="display: inline-block; background-image: url(\'/static/img/icons/bra/bra_all.png\');"></div>' +
		'<div class="selector_title_div" style="display: block;">' +
		    '<div class="selector_title" style="max-width: 553px;">Brasil</div>' +
		    '<div class="selector_description"></div>' +
		    '<div class="breadcrumb" style="display: none"><a class="site_crumb" style="color: rgb(136, 136, 136);">Remover este Filtro<i class="fa fa-close"></i></a></div>' +
		    '<button type="button" class="m-l-xs btn btn-primary btn-outline btn-toggle" style="position: absolute; right: 0; top: 13px;">' + 
		        'Selecione' + 
		    '</button>' + 
		'</div>';

		var groupWidget = '' + 
		'<div class="selector_depth btn-group">' +
		    '<button value="regions" 		class="btn btn-default" name="selector_depth_toggle" >Regiões</button>' +
		    '<button value="states" 		class="btn btn-default" name="selector_depth_toggle" >Estados</button>' +
		    '<button value="mesoregions" 	class="btn btn-default" name="selector_depth_toggle" >Mesorregiões</button>' +
		    '<button value="microregions" 	class="btn btn-default" name="selector_depth_toggle" >Microrregiões</button>' +
		    '<button value="municipalities" class="btn btn-default active" name="selector_depth_toggle" >Municípios</button>' +
		'</div>';

		var searchWidget = '' +
		'<div class="leon text">' +
		    '<input type="text" class="form-control" id="search-input" placeholder="PESQUISE">' +
		'</div>';

		var itemWidget = '' + 
		'<div class="search_result" data-id="{{id}}" data-type="{{type}}" data-name="{{name}}" data-icon="{{icon}}" >' +
			'<div class="search_icon" style="background-image: url(\'{{icon}}\');"></div>' +
		    '<div class="search_text">' +
		        '<div class="search_title" style="color: rgb(47, 47, 109);">{{name}}</div>' +
		        '<div class="search_data">ID: {{id}}</div>' +
		        '<div class="search_data">População: 11,4 Milhões</div>' +
		        '<div class="selector_depth_links">Mostrar: ' +
		        	'{{depth-links}}' +
		        '</div>' +
		    '</div>' +
		    '<button type="button" class="m-l-xs btn btn-primary btn-outline btn-toggle" style="position: absolute; right: 15px; top: 13px;">' + 
		        'Selecione' + 
		    '</button>' + 
		'</div>' +
		'<div class="d3plus_tooltip_data_seperator"></div>';

		var establishmentWidget = '' + 
		'<div class="search_result" >' +
			'<div class="icon-box"><i class="search_icon dv-university-t" style="color: rgb(158, 218, 229);"></i></div>' +
		    '<div class="search_text">' +
		        '<div class="search_title" style="color: rgb(47, 47, 109);">{{name}}</div>' +
		        '<div class="search_data">ID: {{id}}</div>' +
		    '</div>' +
		    '<a href="/en/health/{{id}}" class="m-l-xs btn btn-primary btn-outline btn-toggle" style="position: absolute; right: 0; top: 13px;">' + 
		        'Selecione' + 
		    '</a>' + 
		'</div>' +
		'<div class="d3plus_tooltip_data_seperator"></div>';


		var selectorTemplate = '' + 
		'<div class="selector">' +
			'<div class="selector_header"></div>' +
			'<div class="selector_body" id="contentArea"></div>' +
		'</div>';

		return {
			filterWidget: filterWidget,
			groupWidget: groupWidget,
			searchWidget: searchWidget,
			itemWidget: itemWidget,
			establishmentWidget: establishmentWidget,
			selectorTemplate: selectorTemplate
		};
	})();

	var Modal = (function(){
		var buildModal = function(){
			$('#modal-selector .modal-header h4.modal-title').html('Estabelecimentos')
			$('#modal-selector-content').empty();
			$('#modal-selector-content').append($(Template.selectorTemplate));
			$('#modal-selector-content .selector_header').append($(Template.filterWidget));
			$('#modal-selector-content .selector_header').append($(Template.groupWidget));
			$('#modal-selector-content .selector_header').append($(Template.searchWidget));
		};

		var show = function(){
			buildModal();
			$('#modal-selector').modal('show');
			var loading = dataviva.ui.loading('#modal-selector-content').text('Carregando');

			clusterize = new Clusterize({
				scrollId: 'contentArea',
				contentId: 'contentArea'
			});

			Metadata.get('municipality').then(function(response){
				Data.buildData(response);
				
				items = data.municipalities;
				render();

				$('.selector_body').on('click', '.search_result button', Establishments.get);
				Filter.byInput();
				loading.hide();
			});
		};

		var render = function(){
			var itemsToString = function(){
				var list = [];

				items.forEach(function(x){
					var item = Template.itemWidget
						.replace(/{{name}}/g, x.name_pt)
						.replace(/{{id}}/g, x.id)
						.replace(/{{icon}}/g, x.icon)
						.replace(/{{type}}/g, x.type)

					switch(x.type) {
						case 'region': 	    item = item.replace(/{{depth-links}}/g, '<a class="group-selector" data-group="states">Estados</a>' + '<a class="group-selector" data-group="mesoregions">Mesorregiões</a>' + '<a class="group-selector" data-group="microregions">Microrregiões</a>' + '<a class="group-selector" data-group="municipalities">Municípios</a>'); break;
						case 'state': 	    item = item.replace(/{{depth-links}}/g, '<a class="group-selector" data-group="mesoregions">Mesorregiões</a>' + '<a class="group-selector" data-group="microregions">Microrregiões</a>' + '<a class="group-selector" data-group="municipalities">Municípios</a>'); break;
						case 'mesoregion':  item = item.replace(/{{depth-links}}/g, '<a class="group-selector" data-group="microregions">Microrregiões</a>' + '<a class="group-selector" data-group="municipalities">Municípios</a>'); break;
						case 'microregion': item = item.replace(/{{depth-links}}/g, '<a class="group-selector" data-group="municipalities">Municípios</a>'); break;
						default: item = item.replace(/Mostrar: {{depth-links}}/g, '');
					}

					list.push(item)
				})

				return list;
			};

			clusterize.update(itemsToString());
			clusterize.refresh();
		}

		return {
			show: show,
			render: render
		};
	})();

	var Filter = (function(){
		var setIcon = function(imageUrl){
			$('.selector_header_icon').css("background-image", "url(" + imageUrl + ")");
		};

		var setName = function(name){
			$('.selector_title').html(name);
		};

		var hideBreadcrumb = function(){
			$('.selector_title_div .breadcrumb').hide();
		};

		var showBreadcrumb = function(){
			$('.selector_title_div .breadcrumb').show();
		};

		var reset = function(){
			setIcon('/static/img/icons/bra/bra_all.png');
			setName('Brasil');
			hideBreadcrumb();

			var selectedGroup = $('.selector_depth.btn-group .active').val();
			groupBy(selectedGroup);
		};


		var groupBy = function(group){
			items = data[group];
		};

		var byId = function(id){
			// FIX METHOD

			items = items.filter(function(item){
				try {
					return item.id.startsWith(id);
				} catch(e){
					debugger
				}
			})
		};

		var byInput = function(){
			$('#search-input').on('keyup', function(el){
				var query = el.target.value.toLowerCase();
				
				document.querySelectorAll('#modal-selector-content .search_title').forEach(function(item){
					var text = item.innerHTML.toLowerCase();
					if(text.indexOf(query) == -1)
						item.closest('.search_result').style.display = 'None';
					else
						item.closest('.search_result').style.display = 'block';
				});
			})
		};

		var group = function(item){
			setName(item.name);
			setIcon(item.icon);
			showBreadcrumb()
		}

		return {
			groupBy: groupBy,
			byId: byId,
			group: group,
			reset: reset,
			byInput: byInput
		};

	})();

	var Establishments = (function(){
		var get = function(el){
			var $item = $(el.target).closest('.search_result');
			var id = $item.data('id');
			var type = $item.data('type');

			var loading = dataviva.ui.loading('#modal-selector-content').text('Carregando');

			$.getJSON('http://api.staging.dataviva.info/cnes/id/name_pt?' + type + '=' + id, function(data){
				var establishments = buildData(data);
				load(establishments);
				loading.hide();
			});
		};

		var load = function(establishments){
			establishments = establishments.map(function(x){
				return Template.establishmentWidget
					.replace(/{{name}}/g, x.name_pt)
					.replace(/{{id}}/g, x.id)
			})

			clusterize.update(establishments);
			clusterize.refresh();
		};

		var reset = function(){

		};

		var buildData = function(responseApi){

		    var getAttrByName = function(item, attr){
		        var index = headers.indexOf(attr);
		        return item[index];
		    }

		    var headers = responseApi.headers;
		    var data = [];

		    responseApi.data.forEach(function(item){
		        var dataItem = {};

		        headers.forEach(function(header){
		            dataItem[header] = getAttrByName(item, header);
		        });

		        data.push(dataItem);
		    });

		    return data;
		}

		return {
			get: get
		}

	})();

	var Data = (function(){
		var buildData = function(response){
			var municipalities = {};
			var microregions = {};
			var mesoregions = {};
			var states = {};
			var regions = {};

			for(var key in response) {
				var municipality = response[key];
				var item = {
					icon: getIcon(municipality),
					population: 123,
				};

				municipalities[key] = Object.assign(municipality, item, {type: 'municipality'});
				microregions[municipality.microregion.id] = Object.assign(municipality.microregion, item, {type: 'microregion'});
				mesoregions[municipality.mesoregion.id] = Object.assign(municipality.mesoregion, item, {type: 'mesoregion'});
				states[municipality.state.id] = Object.assign(municipality.state, item, {type: 'state'});
				regions[municipality.region.id] = Object.assign(municipality.region, item, {type: 'region'});
			}

			data.municipalities = [];
			data.microregions = [];
			data.mesoregions = [];
			data.states = [];
			data.regions = [];

			for(key in municipalities){
				data.municipalities.push(municipalities[key]);
			}

			for(key in microregions){
				data.microregions.push(microregions[key]);
			}

			for(key in mesoregions){
				data.mesoregions.push(mesoregions[key]);
			}

			for(key in states){
				data.states.push(states[key]);
			}

			for(key in regions){
				data.regions.push(regions[key]);
			}

			data.mesoregions = data.mesoregions.slice(0, -1); // BUG

			data.municipalities.sort(compare);
			data.microregions.sort(compare);
			data.mesoregions.sort(compare);
			data.states.sort(compare);
			data.regions.sort(compare);
		}

		var compare = function(a,b) {
		  if (a.name_pt < b.name_pt)
		    return -1;
		  if (a.name_pt > b.name_pt)
		    return 1;
		  return 0;
		};

		var getIcon = function(municipality){
			var oldRegion = {
		        "1": "1",
		        "2": "2",
		        "3": "4",
		        "4": "5",
		        "5": "3"
		    }[municipality.region.id];

			return "/static/img/icons/bra/bra_" + oldRegion + municipality.state.abbr_en.toLowerCase() + ".png";
		};

		return {
			buildData: buildData
		}

	})();

	var Events = (function(){
		var addGroupSelector = function(){
			$('#modal-selector-content').on('click', '.group-selector', function(ev){
				var $item = $(ev.target).closest('.search_result');
				var itemId = $item.data('id');
				var itemType = $item.data('type');

				var filterGroup = $(ev.target).data('group');

				Filter.groupBy(filterGroup);
				Filter.byId(itemId);


				$('.selector_depth.btn-group .active').removeClass('active');
				$('.selector_depth.btn-group button[value=' + filterGroup + ']').addClass('active');

				Filter.group({name: $item.data('name'), icon: $item.data('icon')});
				Modal.render();
			})

			$('#modal-selector-content').on('click', '.breadcrumb a', function(ev){
				Filter.reset();
				Modal.render();
			});
		};

		var addDepthSelector = function(){
			$('#modal-selector-content').on('click', '.selector_depth button', function(ev){
				var $button = $(ev.target);

				$button.closest('div').find('.active').removeClass('active');
				$button.addClass('active');

				var group = $button.val();

				Filter.groupBy(group);
				Modal.render();
			});
		};

		return {
			addGroupSelector: addGroupSelector,
			addDepthSelector: addDepthSelector
		};
	})();

	Events.addGroupSelector();
	Events.addDepthSelector();

	return {
		show: Modal.show,
		getEstablishments: Establishments.get
	}
})();