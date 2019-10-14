var notDefined = 'None';

function addMainOccupationJobs(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/year/occupation_family/?order=jobs&' + filters,
        label: {
            metadata: true,
            value: 'occupation_family'
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

function addOccupationWithHighestAverageWage(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/year/occupation_family/?order=average_wage&' + filters,
        prefix: 'R$',
        label: {    
            metadata: true,
            value: 'occupation_family'
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

function addMunicipalityWithHighestAverageWage(filters, id, tab) {
     var query = {
        url: dataviva.api_url + 'rais/municipality/?order=average_wage&' + filters,
        prefix: 'R$',
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
    var idLen = industryId.length;
    var industrys = {
        1: "industry_section",
        3: "industry_division",
        6: "industry_class"
    }

    if(!industryId || industryId === notDefined || !industrys[idLen]) {
        return '';
    }

    var id = idLen === 1 ? industryId : industryId.replace(/\D/g,'');

    return  industrys[idLen] + '=' + id;
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
    var filters = filterBiggest + year + industryFilter + '&' + locationFilter;

    addMainOccupationJobs(filters, id, tab);

    if(!isMunicipality) {
        addMainMunicipalityJobs(filters, id, tab);;
    }

    addOccupationWithHighestAverageWage(filters, id, tab)

    if(!isMunicipality) {
        addMunicipalityWithHighestAverageWage(filters, id, tab);
    }
});
