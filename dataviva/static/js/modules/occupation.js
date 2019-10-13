$(document).ready(function () {

    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    var occupations = {
        1: "occupation_group",
        4: "occupation_family"
    }

    var idIbge = $('#id_ibge').val();
    var locationFilter = isNaN(idIbge) ? '' : `${locations[idIbge.length]}=${idIbge}&`;

    var occupationId = $('#occupation_id').val();
    var occupationFilter = isNaN(occupationId) ? '' : `${occupations[occupationId.length]}=${occupationId}`;

    var isMunicipality = idIbge.length === 7;
    var { pathname } = location;
    var lang = pathname && pathname.split('/')[1];

    var year = "year=2015&";
    var filter = `${year}${locationFilter}${occupationFilter}`;
    var filterBiggest = "limit=1&direction=desc";
    
    var mainMunicipalityJobs = {
        url: dataviva.api_url + `rais/municipality/?order=jobs&${filterBiggest}&${filter}`,
        label: {
            metadata: true,
            value: 'municipality'
        },
        value: 'jobs'
    }

    var mainActivityJobs = {
        url: dataviva.api_url + `rais/year/industry_class/industry_section/industry_division/?order=jobs&${filterBiggest}&${filter}`,
        label: {
            metadata: true,
            value: 'industry_class'
        },
        value: 'jobs'
    }

    var averageWage = {
        url: dataviva.api_url + `rais/municipality/?order=average_wage&${filterBiggest}&${filter}`,
        label: {
            metadata: true,
            value: 'municipality'
        },
        value: 'average_wage',
    }

    // fix query
    var averageMonthlyIncome = {
        url: dataviva.api_url + `rais/year/industry_class/?order=average_wage&${filterBiggest}&${filter}`,
        label: {    
            metadata: true,
            value: 'industry_class'
        },
        value: 'average_wage',
    }

    if(!isMunicipality) {
        General.add({
            ...mainMunicipalityJobs,
            title: dictionary['main_municipality_jobs'],
            id: 'occupation'
        });
        BlueBox.add({
            ...mainMunicipalityJobs,
            title: dictionary['main'],
            subtitle: dictionary['municipality_by_jobs'],
            tab: 'wages'
        });
    }

    General.add({
        ...mainActivityJobs,
        title: dictionary['main_activity_jobs'],
        id: 'occupation'
    });
    BlueBox.add({
        ...mainActivityJobs,
        title: dictionary['main'],
        subtitle: dictionary['activity_jobs'],
        tab: 'wages'
    });

    if(!isMunicipality) {
        General.add({
            ...averageWage,
            title: dictionary['municipality_highest_average_income'],
            id: 'occupation'
        });
        BlueBox.add({
            ...averageWage,
            title: dictionary['principal'],
            subtitle: dictionary['activity_jobs'],
            tab: 'wages'
        });
    }

    General.add({
        ...averageMonthlyIncome,
        title: dictionary['activity_highest_average_income'],
        id: 'occupation'
    });
    BlueBox.add({
        ...averageMonthlyIncome,
        title: dictionary['activity_highest'],
        subtitle: dictionary['average_monthly_income'],
        tab: 'wages'
    });
});
