$(document).ready(function(){
    var filters = location.search.slice(1);

    if(location.pathname.split('/')[2] == 'health')
        filters = 'establishment=' + location.pathname.split('/')[3];

    if(filters.split('=').indexOf('municipality') == -1){
        // BlueBox.add({
        //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?order=beds&direction=desc&limit=1&' + filters,
        //     title: 'Município com Maior',
        //     subtitle: 'Número de Leitos',
        //     label: {
        //         metadata: true,
        //         value: 'municipality'
        //     },
        //     value: 'beds',
        //     suffix: 'Leitos',
        //     tab: 'beds'
        // });

    }
//GENERAL ADD

//ESTABLISHMENT
    // General.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title:  dictionary['total_of_establishments'],
    //     label: '',
    //     value: 'establishments'
    // });

    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_establishments'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'establishments',
    // });

//BED
    General.add({
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title:  dictionary['total_of_beds'],
        label: '',
        value: 'beds'

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_beds'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'beds'
    // });

//PROFESSIONAL
    General.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title:  dictionary['total_of_professionals'],
        label: '',
        value: 'professionals',
        prefix: dictionary['total_of_professionals'] + ' '

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_professionals'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'professionals',
    //     prefix: 'Total of profissionais'
    // });

//EQUIPMENT
    General.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['total_of_equipments'],
        label: '',
        value: 'equipments',
        prefix: dictionary['total_of_equipments'] + ' '

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_equipments'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'equipments'
    // });
    // ESTABLISHMENTS

    // BlueBox.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title: 'Total de Estabelecimentos',
    //     label: 'Total de Estabelecimentos',
    //     value: 'establishments',
    //     tab: 'establishments'
    // });

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Estabelecimentos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'establishments',
    //     suffix: 'Estabelecimentos',
    //     tab: 'establishments'
    // });

    // BlueBox.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/unit_type/?year=2015&" + filters,
    //     title: 'Principal Tipo Estabelecimento',
    //     subtitle: 'por Quantidade',
    //     label: {
    //         metadata: true,
    //         value: 'unit_type'
    //     },
    //     value: 'establishments',
    //     tab: 'establishments'
    // });

    // BEDS

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Leitos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'beds',
    //     suffix: 'Leitos',
    //     tab: 'beds'
    // });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/cnes_bed/year/bed_type/?year=2015&order=beds&direction=desc&limit=1&' + filters,
        title: dictionary['main_bed_type'],
        subtitle: dictionary['by_quantity'],
        label: {
            metadata: true,
            value: 'bed_type'
        },
        value: 'beds',
        tab: 'beds'
    });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title: dictionary['total_of_beds'],
        label: dictionary['total_of_beds'],
        value: 'beds',
        tab: 'beds'
    });

    // PROFESSIONALS

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Profissionais',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'professionals',
    //     suffix: 'Profissionais',
    //     tab: 'professionals'
    // });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/cnes_professional/year/occupation_family/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
        title: dictionary['main_occupation'],
        subtitle: dictionary['by_jobs'],
        label: {
            metadata: true,
            value: 'occupation_family'
        },
        value: 'professionals',
        tab: 'professionals'
    });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title: dictionary['total_of_professionals'],
        label: dictionary['total_of_professionals'],
        value: 'professionals',
        tab: 'professionals'
    });

    // EQUIPMENTS

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['total_of_equipments'],
        label: dictionary['total_of_equipments'],
        value: 'equipments',
        tab: 'equipments'
    });

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Equipamentos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'equipments',
    //     suffix: 'Equipamentos',
    //     tab: 'equipments'
    // });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/equipment_type/?year=2015&" + filters,
        title: dictionary['main_equipment_type'],
        subtitle: dictionary['by_quantity'],
        label: {
            metadata: true,
            value: 'equipment_type'
        },
        value: 'equipments',
        suffix: dictionary['equipments'],
        tab: 'equipments'
    });


//INDICATOR ADD

    //LEITOS
    Indicator.add({
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title: dictionary['number_beds'],
        value:  'beds'
    });

    //EQUIPAMENTOS
    Indicator.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['number_equipments'],
        value:  'equipments'
    });

    //PROFISSIONAIS
    Indicator.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title: dictionary['number_professionals'],
        value:  'professionals'
    });

    //ESTABELECIMENTOS
    // Indicator.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title: dictionary.number_establishments,
    //     value:  'establishments'
    // });
    //


})

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
        $('#general-' + data.value).append(data.template);

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
