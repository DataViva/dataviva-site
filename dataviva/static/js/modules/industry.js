var notDefined = 'None';

// Ocupação com maior número de empregos
function addMainOccupationJobs(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/year/industry_class/industry_section/industry_division/?order=jobs&' + filters,
        label: {
            metadata: true,
            value: 'industry_class'
        },
        value: 'jobs'
    }

    General.add(
        $.extend({}, query, { title: dictionary['occupation'] + ' ' + dictionary['with_more_jobs'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['occupation'], subtitle: dictionary['with_more_jobs'], tab })
    );
}

// Município com maior número de empregos
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
        $.extend({}, query, { title: dictionary['municipality'] + ' ' + dictionary['with_more_jobs'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['municipality'], subtitle: dictionary['with_more_jobs'], tab })
    );
}

// Ocupação com maior renda média mensal
function addOccupationWithHighestAverageWage(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/year/industry_class/?order=average_wage&' + filters,
        label: {    
            metadata: true,
            value: 'industry_class'
        },
        value: 'average_wage',
    }

    General.add(
        $.extend({}, query, { title: dictionary['occupation'] + ' ' + dictionary['highest_average_income'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['occupation'], subtitle: dictionary['highest_average_income'], tab })
    );
}

// Município com maior renda média mensal
function addMunicipalityWithHighestAverageWage(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/municipality/?order=average_wage&' + filters,
        label: {
            metadata: true,
            value: 'municipality'
        },
        value: 'average_wage',
    }

    General.add(
        $.extend({}, query, { title: dictionary['municipality'] + '' + dictionary['highest_average_income'], id })
    );
    BlueBox.add(
        $.extend({}, query, { title: dictionary['municipality'], subtitle: dictionary['highest_average_income'], tab })
    );
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

function getIndustryFilter(industryId) {
    var industrys = {
        1: "industry_section",
        3: "industry_division",
        6: "class"
    }

    return industryId && industryId === notDefined ? '' : industrys[industryId.length] + '=' + industryId;
}

$(document).ready(function () {
    var idIbge = $('#id_ibge').val();
    var locationFilter = getLocationFilter(idIbge);

    var industryId = $('#industry_id').val();
    var industryFilter = getIndustryFilter(industryId);

    var isMunicipality = idIbge.length === 7;
    var pathname = location.pathname;
    var lang = pathname && pathname.split('/')[1];

    var tab = 'wages';
    var id = 'industry';

    var year = "year=2015&";
    var filterBiggest = "limit=1&direction=desc&";
    var filters = filterBiggest + year + locationFilter + industryFilter;

    addMainOccupationJobs(filters, id, tab);

    if(!isMunicipality) {
        addMainMunicipalityJobs(filters, id, tab);;
    }

    addOccupationWithHighestAverageWage(filters, id, tab)

    if(!isMunicipality) {
        addMunicipalityWithHighestAverageWage(filters, id, tab);
    }
});
