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
	        url: 'http://api.staging.dataviva.info/hedu/year/municipality?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
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
	        url: 'http://api.staging.dataviva.info/hedu/year/municipality?order=entrants&year=2015&direction=desc&limit=1&' + filter,
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
	        url: 'http://api.staging.dataviva.info/hedu/year/municipality?order=graduates&year=2015&direction=desc&limit=1&' + filter,
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
        url: 'http://api.staging.dataviva.info/hedu/year/university?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
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
        url: 'http://api.staging.dataviva.info/hedu/year/university?order=entrants&year=2015&direction=desc&limit=1&' + filter,
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
        url: 'http://api.staging.dataviva.info/hedu/year/university?order=graduates&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_university'],
        subtitle: dictionary['number_graduates_students'],
        label: {
            metadata: true,
            value: 'university'
        },
        value: 'graduates',
        tab: 'enrollments'
    });

});