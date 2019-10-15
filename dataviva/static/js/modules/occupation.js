var notDefined = 'None';

function addMainMunicipalityJobs(filters, id, tab) {
    var query = {
        url: dataviva.api_url + 'rais/municipality/?order=jobs&' + filters,
        label: {
            metadata: true,
            value: 'municipality'
        },
        value: 'jobs'
    }

    General.add(
        $.extend({}, query, { title: dictionary['main_municipality_jobs'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['main'], subtitle: dictionary['municipality_by_jobs'], tab })
    );
}

function addMainActivityJobs(filters, id, tab) {
    var query = {
        url: dataviva.api_url + 'rais/year/industry_class/industry_section/industry_division/?order=jobs&' + filters,
        label: {
            metadata: true,
            value: 'industry_class'
        },
        value: 'jobs'
    }

    General.add(
        $.extend({}, query, { title: dictionary['main_activity_jobs'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['main'], subtitle: dictionary['activity_jobs'], tab })
    );
}

function addAverageWage(filters, id, tab) {
    var query = {
        url: dataviva.api_url + 'rais/municipality/?order=average_wage&' + filters,
        label: {
            metadata: true,
            value: 'municipality'
        },
        value: 'average_wage',
    }

    General.add(
        $.extend({}, query, { title: dictionary['municipality_highest_average_income'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['principal'], subtitle: dictionary['activity_jobs'], tab })
    );
}

function addAverageMonthlyIncome(filters, id, tab) {
    var query = {
        url: dataviva.api_url + 'rais/year/industry_class/?order=average_wage&' + filters,
        label: {    
            metadata: true,
            value: 'industry_class'
        },
        value: 'average_wage',
    }

    General.add(
        $.extend({}, query, { title: dictionary['activity_highest_average_income'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['activity_highest'], subtitle: dictionary['average_monthly_income'], tab })
    );
}

function addIndicators(filters) {
    Indicator.add({
        url: dataviva.api_url + "rais/year/?" + filters,
        title: dictionary['average_income'] + ' (2017)',
        prefix: 'R$',
        value:  'average_wage'
    });
    Indicator.add({
        url: dataviva.api_url + "rais/year/?" + filters,
        title: dictionary['payroll'] + ' (2017)',
        prefix: 'R$',
        value:  'wage'
    });
    Indicator.add({
        url: dataviva.api_url + "rais/year/?" + filters,
        title: dictionary['total_employment'] + ' (2017)',
        value:  'jobs'
    });
    Indicator.add({
        url: dataviva.api_url + "rais/year/?count=establishment&" + filters,
        title: dictionary['total_establishments'] + ' (2017)',
        value:  'establishment_count'
    });
}

function getLocationFilter(idIbge) {
    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    return isNaN(idIbge) ? '' : locations[idIbge.length] + '=' + idIbge;
} 

function getOccupationFilter(occupationId) {
    var idLen = occupationId.length;
    var occupations = {
        1: "occupation_group",
        4: "occupation_family"
    }

    if(!occupationId || occupationId === notDefined || !occupations[idLen]) {
        return '';
    }

    return  occupations[idLen] + '=' + occupationId;
}

$(document).ready(function () {
    var id = 'occupation';
    var tab = 'wages';

    var idIbge = $('#id_ibge').val();
    var locationFilter = getLocationFilter(idIbge);

    var occupationId = $('#occupation_id').val();
    var occupationFilter = getOccupationFilter(occupationId);

    var isMunicipality = idIbge.length === 7;
    var pathname = location.pathname;
    var lang = pathname && pathname.split('/')[1];

    var year = 'year=2017&';
    var filterBiggest = 'limit=1&direction=desc&';
    var filters = filterBiggest + year + occupationFilter + '&' + locationFilter;

    addIndicators(filters);

    if(!isMunicipality) {
        addMainMunicipalityJobs(filters, id, tab)
    }

    addMainActivityJobs(filters, id, tab)

    if(!isMunicipality) {
        addAverageWage(filters, id, tab);
    }

    addAverageMonthlyIncome(filters, id, tab);
});
