
var lang = location.pathname.split('/')[1];

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
                    api = buildData(response);
                }
            }),

            !data.label.metadata ? undefined : getMetadata(data.label.value).then(function(response){
                metadata = response;
            })
        ).then(function() {

            if(api[0] == undefined){
                data.template.hide();
                return;
            }

            var label = data.label;
            if (typeof data.label == 'object') {
                if (typeof data.label.funct == 'function') {
                    label = data.label.funct(api, metadata);
                } else {
                   label = metadata[api[0][data.label.value]]['name_' + lang];
                }
            }

            if (typeof data.label == 'function') {
                label = data.label(api, metadata);
            }

            var formattedValue;

            if (typeof data.value == 'function'){
                formattedValue = data.value(api);
                formattedValue = Magnitude(formattedValue)
            }
            else {
                formattedValue = Magnitude(api[0][data.value]);
            }

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

                var formattedValue;

                if (typeof data.value == 'function'){
                    formattedValue = data.value(buildData(response));
                    formattedValue = Magnitude(formattedValue)
                }
                else {
                    formattedValue = Magnitude(api[data.value]);
                }

                var value = formattedValue.split(' ')[0].replace('.', ',');
                var magnitude = formattedValue.split(' ')[1] || '';
                
                var filledTemplate = template.replace('{{title}}', data.title || '')
                                    .replace('{{value}}', value)
                                    .replace('{{magnitude}}', magnitude)
                                    .replace('{{preffix}}', data.preffix || '' )
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
    '<div class="col-xs-12 col-sm-6 col-md-4 col-lg-3">' +
        '<div class="blue-box title blue-box--loading">' +
            '{{title}}' +
            '<small>{{subtitle}}</small>' +
        '</div>' +
        '<div class="blue-box blue-box--loading">' +
            '<p class="label">{{label}}</p>' +
            '<div class="number">' +
                '<small>{{prefix}}</small><strong class="counter">{{value}}</strong><span>{{magnitude}} {{suffix}}</span>' +
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
                    api = buildData(response);
                }           
            }),

            !data.label.metadata ? undefined : getMetadata(data.label.value).then(function(response){
                metadata = response;
            })
        ).then(function() {
            if(api[0] == undefined){
                data.template.hide();
                return;
            }

            var label = data.label;
            if (typeof data.label == 'object') {
                if (typeof data.label.funct == 'function') {
                    label = data.label.funct(api, metadata);
                } else {
                   label = metadata[api[0][data.label.value]]['name_' + lang];
                }
            }

            if (typeof data.label == 'function') {
                label = data.label(api, metadata);
            }

            var formattedValue;

            if (typeof data.value == 'function'){
                formattedValue = data.value(api);
                formattedValue = Magnitude(formattedValue)
            }
            else {
                formattedValue = Magnitude(api[0][data.value]);
            }

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
    var nAbs = Math.abs(n);
    if (nAbs < 1000)
        return n + '';
    if (nAbs < 1000000)
        return (n/1000).toPrecision(3) + ' ' + dictionary.thousand;
    if (nAbs < 1000000000)
        return nAbs < 2000000 ? (n/1000000).toPrecision(3) + ' ' + dictionary.million : (n/1000000).toPrecision(3) + ' ' + dictionary.millions;
    if (nAbs < 1000000000000)
        return nAbs < 2000000000 ? (n/1000000000).toPrecision(3) + ' ' + dictionary.billion : (n/1000000000).toPrecision(3) + ' ' + dictionary.billions;
    if (nAbs < 1000000000000000)
        return nAbs < 2000000000000 ? (n/1000000000000).toPrecision(3) + ' ' + dictionary.trillion : (n/1000000000000).toPrecision(3) + ' ' + dictionary.trillions;
};