var data = [],
    lang = document.documentElement.lang,
    dataset = $("#radar").attr("dataset"),
    polygon = $("#radar").attr("polygon"),
    label = $("#radar").attr("label"),
    value = $("#radar").attr("value"),
    filters = $("#radar").attr("filters"),
    url = "http://api.staging.dataviva.info/" + 
        dataset + "/year/" + polygon + "/" + label + ( filters ? "?" + filters : '');

var titleHelper = {
    'jobs': {
        'en': 'Jobs in ',
        'pt': 'Empregos em '
    },
    'average_monthly_wage': {
        'en': 'Average Monthly Wage in ',
        'pt': 'Salário Médio Mensal em '
    },
    'gender': {
        'en': ' by gender',
        'pt': ' por gênero'
    },
    'pageTitle': window.parent.document.querySelector('h1').childNodes[0].textContent.replace(/\s+/g,' ').trim()
}

var title = titleHelper[value][lang] + titleHelper.pageTitle + titleHelper.gender[lang];

$('#title').html(title);


var loading = dataviva.ui.loading('.loading');
if (lang == "en") {
    loading.text('loading' + "...");
} else {
    loading.text('carregando' + "...");
}

var compare = function(a, b){
    if(a.year < b.year)
        return -1;
    if(a.year > b.year)
        return 1;

    if(a[label] < b[label])
        return -1;
    if(a[label] > b[label])
        return 1;

    return 0;
}

var tooltipTemplate = '<div id="d3plus_tooltip_id_visualization_focus" class="d3plus_tooltip d3plus_tooltip_small" style="color: rgb(68, 68, 68); font-family: "Helvetica Neue"; font-weight: 200; font-size: 12px; box-shadow: rgba(0, 0, 0, 0.247059) 0px 1px 3px; position: absolute; max-height: 610px; z-index: 2000; top: 7px; left: 721px;"> <div class="d3plus_tooltip_container" style="background-color: rgb(255, 255, 255); padding: 6px; width: 236px;"> <div class="d3plus_tooltip_header" style="position: relative; z-index: 1;"> <div class="d3plus_tooltip_title" style="max-width: 244px; color: rgb(40, 47, 107); vertical-align: top; width: 220px; display: inline-block; overflow: hidden; text-overflow: ellipsis; word-wrap: break-word; z-index: 1; font-size: 16px; line-height: 17px; padding: 3px;">{{title}}</div></div><div class="d3plus_tooltip_data_container" style="overflow-y: auto; z-index: -1; max-height: 151px;"> <div class="d3plus_tooltip_data_block" style="font-size: 12px; padding: 3px 6px; position: relative; color: rgb(0, 0, 0);"> <div class="d3plus_tooltip_data_name" style="display: inline-block; width: 156.641px; min-height: 15px;">{{male_label}}</div><div class="d3plus_tooltip_data_value" style="display: block; position: absolute; text-align: right; top: 3px; right: 6px; ">{{male_data}}</div></div><div class="d3plus_tooltip_data_seperator" style="background-color: rgb(221, 221, 221); display: block; height: 1px; margin: 0px 3px;"></div><div class="d3plus_tooltip_data_block" style="font-size: 12px; padding: 3px 6px; position: relative; color: rgb(0, 0, 0);"> <div class="d3plus_tooltip_data_name" style="display: inline-block; width: 156.641px; min-height: 15px;">{{female_label}}</div><div class="d3plus_tooltip_data_value" style="display: block; position: absolute; text-align: right; top: 3px; right: 6px; ">{{female_data}}</div></div></div><div class="d3plus_tooltip_footer" style="font-size: 10px; position: relative; text-align: center;"></div></div></div>';

var avg = function(items, attr){
    var sum = items.reduce(function(acc, item){ return acc + item[attr]; }, 0);

    if(items.length == 0)
        return 0;

    return sum / items.length;
}

var sum = function(items, attr){
    return items.reduce(function(acc, item){ return acc + item[attr]; }, 0);
}

var getTooltipData = function (data, label, years){
    var filteredData = data.filter(function(item){
        return years.indexOf(item.year) != -1 && item.name.toLowerCase() == label.toLowerCase();
    });

    var maleData = filteredData.filter(function(item){
        if(lang == 'en' && item.gender == 'Male')
            return true;
        if(lang == 'pt' && item.gender == 'Homem')
            return true;

        return false;
    });

    var femaleData = filteredData.filter(function(item){
        if(lang == 'en' && item.gender == 'Female')
            return true;
        if(lang == 'pt' && item.gender == 'Mulher')
            return true;

        return false;
    });

    var tooltipData = {
        'male': {},
        'female': {}
    };

    tooltipData.male[value] = sum(maleData, value);
    tooltipData.female[value] = sum(femaleData, value);

    return tooltipData;
}

var formatTooltipData = function(tooltipData){
    if(value == 'jobs'){
        tooltipData.male.jobs = d3plus.number.format(tooltipData.male.jobs);
        tooltipData.female.jobs = d3plus.number.format(tooltipData.female.jobs);
    }
    else if(value == 'average_monthly_wage'){
        tooltipData.male.average_monthly_wage = '$' + d3plus.number.format(tooltipData.male.average_monthly_wage) + ' USD';
        tooltipData.female.average_monthly_wage = '$' + d3plus.number.format(tooltipData.female.average_monthly_wage) + ' USD';
    }

    return tooltipData;
}

var getSelectedYears = function() {
    var years = $('#timeline #labels [fill="rgba(68,68,68,1)"]').map(function (index, item){
        return +item.innerHTML
    })

    years = Array.from(years);
    return years;
}

var getLabelName = function(element) {
    var texts = $(element).find("tspan").map(function (index, tspan){
        return $(tspan).html();
    });

    texts = Array.from(texts);
    var label = texts.join(" ");

    return label;
}

var updateTooltip = function(element){
    var years = getSelectedYears();
    var label = getLabelName(element);
    var tooltipData = getTooltipData(data, label, years);
    tooltipData = formatTooltipData(tooltipData);

    var html = tooltipTemplate
        .replace('{{title}}', label)
        .replace('{{male_label}}', lang == 'en' ? 'Male' : 'Homem')
        .replace('{{male_data}}', tooltipData.male[value])
        .replace('{{female_label}}', lang == 'en' ? 'Female' : 'Mulher')
        .replace('{{female_data}}', tooltipData.female[value]);

    $('#tooltip').html(html);
}

var showTooltip = function() {
    $('#tooltip').css('display', 'block');
    $('#tooltip').css('position', 'fixed');
    $('#tooltip').css('overflow', 'hidden');
};

var hideTooltip = function() {
    $('#tooltip').css('display', 'none');
};

var addTooltipToLabels = function(){
    if($('.d3plus_radar_labels').length == 0){
        setTimeout(addTooltipToLabels, 1000);
        return;
    }

    $('.d3plus_radar_labels').hover(function(event) {
        updateTooltip(this);
    });

    $('.d3plus_radar_labels').hover(showTooltip, hideTooltip);
};

window.onmousemove = function (e) {
    var tooltip = $('#tooltip');

    var windowSize = {
        x: $(window).width(),
        y: $(window).height()
    };

    var tooltipSize = {
        x: $(tooltip).width(),
        y: $(tooltip).height()
    };

    var cursorPosition = {
        x: e.clientX,
        y: e.clientY
    };

    var offset = 10;

    if(cursorPosition.x + tooltipSize.x + offset > windowSize.x){
        $('#tooltip').css('left', (cursorPosition.x - offset - tooltipSize.x) + 'px');
    }
    else {
        $('#tooltip').css('left', (cursorPosition.x + offset) + 'px');
    }

    if(cursorPosition.y + tooltipSize.y + offset > windowSize.y){
        $('#tooltip').css('top', (cursorPosition.y - offset - tooltipSize.y) + 'px');
    }
    else {
        $('#tooltip').css('top', (cursorPosition.y + offset) + 'px');
    }

};

$(document).ready(function(){
    ajaxQueue([
        url,
        "http://api.staging.dataviva.info/metadata/" + polygon,
        "http://api.staging.dataviva.info/metadata/" + label
    ], 

    function(responses){
        var json = responses[0],
            polygon_metadata = responses[1],
            label_metadata = responses[2];

        json.data.forEach(function(item, index){
            var dataItem = {};

            dataItem["year"] = item[0]
            dataItem[polygon] = item[1]
            dataItem[label] = item[2]
            dataItem["average_monthly_wage"] = +item[5]
            dataItem["jobs"] = item[6]

            data.push(dataItem);
        });

        data.map(function(item){
            item["image"] = item.gender == '1' ? '/static/img/icons/genders/male.png' : '/static/img/icons/genders/female.png'
        });

        data.map(function(item){
            item["name"] = label_metadata[item[label]]["name_" + lang];
            item[polygon] = polygon_metadata[item[polygon]]["name_" + lang];
        });

        data.sort(compare);
        loading.hide();

        var visualization = d3plus.viz()
            .container("#radar")
            .type("radar")
            .data(data)
            .id([polygon, "name"])
            .color({
                "value": polygon,
                "tooltip": "name"
            })
            .size(value)
            .time({
                "value": "year",
                "solo": []
            })
            .icon({
                "style": "knockout",
                "value": "image"
            })
            .background("transparent")
            .format({
                "number": function(number, params) {
                    var formatted = d3plus.number.format(number, params);
                    if (params.key === "average_monthly_wage") {
                        return "$" + formatted + " USD";
                    }
                    else {
                        return formatted;
                    }
                },
                "text": function(text, params) {
                    if (text === "average_monthly_wage") {
                        return lang == 'en' ? 'Average Monthly Wage' : 'Salário Médio Mensal';
                    }
                    else if(text === "jobs") {
                        return lang == 'en' ? 'Jobs' : 'Empregos';
                    }

                    else {
                        return d3plus.string.title(text, params);
                    }

                }
            })
            .draw();

            addTooltipToLabels()
    });
});
