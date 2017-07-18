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
    	courseFilter = 'sc_course_field=' + course;
    else if (course.length == 5)
    	courseFilter = 'sc_course=' + course;

    var idIbge = $('#id_ibge').val();
    var locationFilter = ''
    if (idIbge != 'None')
    	locationFilter = idIbge ? locations[idIbge.length] + '=' + idIbge : '';

    filter = [courseFilter, locationFilter].join('&');
    var isMunicipality = idIbge.length == 7;

    //BLUEBOXES ADD
    if(!isMunicipality){
        BlueBox.add({
            url: 'http://api.staging.dataviva.info/sc/year/municipality?order=students&year=2016&direction=desc&limit=1&' + filter,
            title: dictionary['main_municipality'],
            subtitle: dictionary['number_enrolled_students'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'students',
            tab: 'enrollments'
        });
    }

    //INDICATORS ADD
    Indicator.add({
        url: "http://api.staging.dataviva.info/sc/year?year=2016&" + filter,
        title: dictionary['number_enrolled'] + ' (2016)',
        value:  'students'
    });
    Indicator.add({
        url: "http://api.staging.dataviva.info/sc/year?year=2016&" + filter,
        title: dictionary['number_classes'] + ' (2016)',
        value:  'classes'
    });
    Indicator.add({
        url: "http://api.staging.dataviva.info/sc/year?year=2016&" + filter,
        title: dictionary['number_schools'] + ' (2016)',
        value:  'schools'
    });
    Indicator.add({
        url: "http://api.staging.dataviva.info/sc/year?year=2016&" + filter,
        title: dictionary['average_class_size'] + ' (2016)',
        value:  'average_class_size'
    });
    Indicator.add({
        url: "http://api.staging.dataviva.info/sc/year?year=2016&" + filter,
        title: dictionary['average_age'] + ' (2016)',
        value:  'average_age'
    });

    //GENERAL ADD 
    General.add({
        url: 'http://api.staging.dataviva.info/sc/year/municipality?order=students&year=2016&direction=desc&limit=1&' + filter,
        title: dictionary['main_municipality_students'],
        label: {
                metadata: true,
                value: 'municipality'
            },
        value: 'students',
    });
});