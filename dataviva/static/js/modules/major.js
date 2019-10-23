$(document).ready(function(){
    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    var course = location.pathname.split('/')[3];
    var courseFilter;

    if (course.length == 2)
    	courseFilter = 'hedu_course_field=' + course;
    else if (course.length == 6)
    	courseFilter = 'hedu_course=' + course;

    var idIbge = $('#id_ibge').val();
    var locationFilter = ''
    if (idIbge != 'None')
    	locationFilter = idIbge ? locations[idIbge.length] + '=' + idIbge : '';

    filter = [courseFilter, locationFilter].join('&');
    var isMunicipality = idIbge.length == 7;

    if(!isMunicipality) {
	    BlueBox.add({
	        url: dataviva.api_url + 'hedu/year/municipality/?order=enrolleds&year=2017&direction=desc&limit=1&' + filter,
	        title: dictionary['main_municipality'],
	        subtitle: dictionary['number_enrolled_students'],
	        label: {
	            metadata: true,
	            value: 'municipality'
	        },

	        value: 'enrolleds',
	        tab: 'enrollments'
	    });

	    BlueBox.add({
	        url: dataviva.api_url + 'hedu/year/municipality/?order=entrants&year=2017&direction=desc&limit=1&' + filter,
	        title: dictionary['main_municipality'],
	        subtitle: dictionary['number_entrant_students'],
	        label: {
	            metadata: true,
	            value: 'municipality'
	        },
	        value: 'entrants',
	        tab: 'enrollments'
	    });

	    BlueBox.add({
	        url: dataviva.api_url + 'hedu/year/municipality/?order=graduates&year=2017&direction=desc&limit=1&' + filter,
	        title: dictionary['main_municipality'],
	        subtitle: dictionary['number_graduates_students'],
	        label: {
	            metadata: true,
	            value: 'municipality'
	        },
	        value: 'graduates',
	        tab: 'enrollments'
	    });
	}

    BlueBox.add({
        url: dataviva.api_url + 'hedu/year/university/?order=enrolleds&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university'],
        subtitle: dictionary['number_enrolled_students'],
        label: {
            metadata: true,
            value: 'university'
        },
        value: 'enrolleds',
        tab: 'enrollments'
    });

    BlueBox.add({
        url: dataviva.api_url + 'hedu/year/university/?order=entrants&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university'],
        subtitle: dictionary['number_entrant_students'],
        label: {
            metadata: true,
            value: 'university'
        },
        value: 'entrants',
        tab: 'enrollments'
    });


    BlueBox.add({
        url: dataviva.api_url + 'hedu/year/university/?order=graduates&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university'],
        subtitle: dictionary['number_graduates_students'],
        label: {
            metadata: true,
            value: 'university'
        },
        value: 'graduates',
        tab: 'enrollments'
    });

    //GENERAL ADD
    General.add({
        url: dataviva.api_url + 'hedu/year/university/?order=enrolleds&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university_enrolled'],
        label: {
                metadata: true,
                value: 'university'
            },
        value: 'enrolleds',
        id: 'enrolleds',
    });

    General.add({
        url: dataviva.api_url + 'hedu/year/municipality/?order=enrolleds&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_municipality_students'],
        label: {
                metadata: true,
                value: 'municipality'
            },
        value: 'enrolleds',
        id: 'enrolleds',
    });

    General.add({
        url: dataviva.api_url + 'hedu/year/university/?order=entrants&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university_entrants'],
        label: {
                metadata: true,
                value: 'university'
            },
        value: 'entrants',
        id: 'enrolleds',
    });

    General.add({
        url: dataviva.api_url + 'hedu/year/municipality/?order=entrants&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_municipality_entrants'],
        label: {
                metadata: true,
                value: 'municipality'
            },
        value: 'entrants',
        id: 'enrolleds',
    });

    General.add({
        url: dataviva.api_url + 'hedu/year/university/?order=graduates&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_university_graduates'],
        label: {
                metadata: true,
                value: 'university'
            },
        value: 'graduates',
        id: 'enrolleds',
    });

    General.add({
        url: dataviva.api_url + 'hedu/year/municipality/?order=graduates&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_municipality_graduates'],
        label: {
                metadata: true,
                value: 'municipality'
            },
        value: 'graduates',
        id: 'enrolleds',
    });

    //INDICATORS ADD
    Indicator.add({
        url: dataviva.api_url + "hedu/year/?count=enrollments&year=2017&" + filter,
        title: dictionary['number_enrolleds'] + ' (2017)',
        prefix: 'USD',
        value:  'enrolleds'
    });

    Indicator.add({
        url: dataviva.api_url + "hedu/year/?count=entrants&year=2017&" + filter,
        title: dictionary['number_entrants'] + ' (2017)',
        value:  'entrants'
    });

    Indicator.add({
        url: dataviva.api_url + "hedu/year/?count=graduates&year=2017&" + filter,
        title: dictionary['number_graduates'] + ' (2017)',
        value:  'graduates'
    });

});