
var lang = location.pathname.split('/')[1];
var dictionary = {};

dictionary['total_of_establishments'] = lang == 'en' ? 'Total of Establishments' : 'Total de Estabelecimentos';
dictionary['municipality_with_highest_number_of_establishments'] = lang == 'en' ? 'Municipality with the highest number of Establishments' : 'Município com maior numero de Estabelecimentos';
dictionary['establishments'] = lang == 'en' ? 'establishments' : 'estabelecimentos';

dictionary['total_of_professionals'] = lang == 'en' ? 'Total of Professionals' : 'Total de Profissionais';
dictionary['municipality_with_highest_number_of_professionals'] = lang == 'en' ? 'Municipality with the highest number of Professionals' : 'Município com maior numero de Profissionais';
dictionary['professionals'] = lang == 'en' ? 'professionals' : 'profissionais';

dictionary['total_of_beds'] = lang == 'en' ? 'Total of beds' : 'Total de Leitos';
dictionary['municipality_with_highest_number_of_beds'] = lang == 'en' ? 'Municipality with the highest number of Beds' : 'Município com maior numero de Leitos';
dictionary['beds'] = lang == 'en' ? 'beds' : 'Leitos';

dictionary['total_of_equipments'] = lang == 'en' ? 'Total of equipments' : 'Total de Equipamentos';
dictionary['municipality_with_highest_number_of_equipments'] = lang == 'en' ? 'Municipality with the highest number of equipments' : 'Município com maior numero de Equipamentos';
dictionary['equipments'] = lang == 'en' ? 'Equipments' : 'Equipamentos';

dictionary['number_establishments'] = lang == 'en' ? 'Number of Establishments' : 'Numero de Estabelecimentos';
dictionary['number_beds'] = lang == 'en' ? 'Number of Beds' : 'Numero de Leitos';
dictionary['number_professionals'] = lang == 'en' ? 'Number of Professionals' : 'Numero de Profissionais';
dictionary['number_equipments'] = lang == 'en' ? 'Number of Equipments' : 'Numero de Equipamentos';

dictionary['main_equipment_type'] = lang == 'en' ? 'Main Equipment Type' : 'Principal Tipo Equipamento';

dictionary['main_occupation'] = lang == 'en' ? 'Main Occupation' : 'Principal Ocupação';
dictionary['by_jobs'] = lang == 'en' ? 'by jobs' : 'por empregos';

dictionary['main_bed_type'] = lang == 'en' ? 'Main Bed Type' : 'Principal Tipo Leito';
dictionary['by_quantity'] = lang == 'en' ? 'by quantity' : 'por quantidade';

dictionary['trillion'] = lang == 'en' ? 'Trillion' : 'Trilhão';
dictionary['billion'] = lang == 'en' ? 'Billion' : 'Bilhão';
dictionary['million'] = lang == 'en' ? 'Million' : 'Milhão';

dictionary['trillions'] = lang == 'en' ? 'Trillions' : 'Trilhões';
dictionary['billions'] = lang == 'en' ? 'Billions' : 'Bilhões';
dictionary['millions'] = lang == 'en' ? 'Millions' : 'Milhões';

dictionary['thousand'] = lang == 'en' ? 'Thousand' : 'Mil';


var buildData = function(responseApi){
    var getAttrByName = function(item, attr){
        var index = headers.indexOf(attr);
        return item[index];
    }

    var data = [];
    var headers = responseApi.headers;

    responseApi.data.forEach(function(item){
        var dataItem = {};

        headers.forEach(function(header){
            dataItem[header] = getAttrByName(item, header);
        });

        data.push(dataItem);
    });

    return data;
}

var getMetadata = function(key){
    return new Promise(function(resolve, reject) {
        if (localStorage.getItem(key)) {
            resolve(JSON.parse(localStorage.getItem(key)));
        }
        else {
            $.ajax({
                url: "http://api.staging.dataviva.info/metadata/" + key,
                success: function (data) {
                    localStorage.setItem(key, JSON.stringify(data));
                    resolve(JSON.parse(localStorage.getItem(key)));
                }
            });
        }
    });
}

var General = (function(){
    var template = '' +
          '<dl class="dl-horizontal loading">' +
              '<dt>{{title}}</dt>'+
              '<dd>'+
                '<small>{{label}}</small>'+
                '<strong class="counter">{{preffix}} {{value}} </strong>'+
                '<span> {{magnitude}}</span>'+
              '</dd>'+
          '</dl>';

    var add = function(data){

        var api;
        var metadata;

        data['template'] = $(template);
        $('#general-' + (data.id || data.value)).append(data.template);

        $.when(
            $.ajax({
                url: data.url,
                type: 'GET',
                success: function(response){
                    api = buildData(response)[0];
                }
            }),

            !data.label.metadata ? undefined : getMetadata(data.label.value).then(function(response){
                metadata = response;
            })
        ).then(function() {
            if(api == undefined){
                data.template.hide();
                return;
            }

            var label = data.label;
            if (typeof data.label == 'object')
                label = metadata[api[data.label.value]].name_pt;

            var formattedValue = Magnitude(api[data.value]);
            var value = formattedValue.split(' ')[0].replace('.', ',');
            var magnitude = formattedValue.split(' ')[1] || '';

            var filledTemplate = template.replace('{{title}}', data.title || '')
                                .replace('{{label}}', label.toUpperCase() || '')
                                .replace('{{value}}', value)
                                .replace('{{magnitude}}', magnitude)
                                .replace('{{preffix}}', data.preffix || '' )
                                .replace('dl-horizontal loading', 'dl-horizontal');

            data.template.replaceWith(filledTemplate);
        });
    }

    return {
        add: add
    };
})();

var Indicator = (function(){
    var template = '' +
    '<div class="col-xs-6 col-sm-4 col-md-3 col-lg-2">' +
        '<div class="widget loading">' +
            '<h2 class="text-left text-uppercase">{{title}}</h2>' +
            '<div class="number">' +
                '{{preffix}} <strong class="counter">{{value}}</strong><br/>' +
                '<small class="magnitude">{{magnitude}}</small>' +
            '</div>' +
        '</div>' +
    '</div>';
    
    var add = function(data){
        var api;
        var metadata;

        data['template'] = $(template);
        $('#header .indices .row').append(data.template);

        $.ajax({
            url: data.url,
            type: 'GET',
            success: function(response){
                var api = buildData(response)[0];

                if(api == undefined){
                    data.template.hide();
                    return;
                }

                var formattedValue = Magnitude(api[data.value]);
                var value = formattedValue.split(' ')[0].replace('.', ',');
                var magnitude = formattedValue.split(' ')[1] || '';
                
                var filledTemplate = template.replace('{{title}}', data.title || '')
                                    .replace('{{value}}', value)
                                    .replace('{{magnitude}}', magnitude)
                                    .replace('{{preffix}}', data.prefix || '' )
                                    .replace('loading', '');

                data.template.replaceWith(filledTemplate);
            }
        });
    }

    return {
        add: add
    };
})();

var BlueBox = (function(){
    var template = '' +
    '<div class="col-xs-12 col-sm-6 col-md-4">' +
        '<div class="blue-box title blue-box--loading">' +
            '{{title}}' +
            '<small>{{subtitle}}</small>' +
        '</div>' +
        '<div class="blue-box blue-box--loading">' +
            '<p class="label">{{label}}</p>' +
            '<div class="number">' +
                '<strong class="counter">{{value}}</strong><span>{{magnitude}} {{suffix}}</span>' +
            '</div>' +
        '</div>' +
    '</div>';

    var add = function(data){

        var api;
        var metadata;

        data['template'] = $(template);
        $('#' + data.tab + ' .row').append(data.template);

        $.when(
            $.ajax({
                url: data.url, 
                type: 'GET',    
                success: function(response){
                    api = buildData(response)[0];
                }           
            }),

            !data.label.metadata ? undefined : getMetadata(data.label.value).then(function(response){
                metadata = response;
            })
        ).then(function() {
            if(api == undefined){
                data.template.hide();
                return;
            }

            var label = data.label;
            if (typeof data.label == 'object')
                label = metadata[api[data.label.value]].name_pt;

            var formattedValue = Magnitude(api[data.value]);
            var value = formattedValue.split(' ')[0].replace('.', ',');
            var magnitude = formattedValue.split(' ')[1] || '';

            var filledTemplate = template.replace('{{title}}', data.title || '')
                                .replace('{{subtitle}}', data.subtitle || '')
                                .replace('{{label}}', label.toUpperCase() || '')
                                .replace('{{value}}', value)
                                .replace('{{magnitude}}', magnitude)
                                .replace('{{prefix}}', data.prefix || '' )
                                .replace('{{suffix}}', data.suffix || '')
                                .replace('blue-box--loading', '')
                                .replace('blue-box--loading', '');

            data.template.replaceWith(filledTemplate);
        });       
    }

    return {
        add: add
    };
})();

var Magnitude = function(n){
    if (n < 1000)
        return n + '';
    if (n < 1000000)
        return (n/1000).toPrecision(3) + ' ' + dictionary.thousand;
    if (n < 1000000000)
        return n < 2000000 ? (n/1000000).toPrecision(3) + dictionary.million : (n/1000000).toPrecision(3) + ' ' + dictionary.millions;
    if (n < 1000000000000)
        return n < 2000000000 ? (n/1000000000).toPrecision(3) + dictionary.billion : (n/1000000000).toPrecision(3) + ' ' + dictionary.billions;
    if (n < 1000000000000000)
        return n < 2000000000000 ? (n/1000000000000).toPrecision(3) + dictionary.trillion : (n/1000000000000).toPrecision(3) + ' ' + dictionary.trillions;
};