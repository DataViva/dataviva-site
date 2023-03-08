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
            url: dataviva.api_url + '/sc/year/municipality/?order=students&year=2017&direction=desc&limit=1&' + filter,
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

    BlueBox.add({
        url: dataviva.api_url + '/sc/year/sc_school/?order=students&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_school'],
        subtitle: dictionary['number_enrolled_students'],
        label: {
            funct: function(response) {
                var metadata = '';
                $.ajax({
                    url: dataviva.api_url + '/metadata/sc_school/'+response[0]['sc_school'],
                    type: 'GET',
                    async: false,
                    success: function(school){
                        metadata = school['name_' + lang];
                    }
                });
                return metadata;
            }
        },
        value: 'students',
        tab: 'enrollments'
    });

    //INDICATORS ADD
    Indicator.add({
        url: dataviva.api_url + "/sc/year/?year=2017&" + filter,
        title: dictionary['number_enrolled'] + ' (2017)',
        value:  'students'
    });
    Indicator.add({
        url: dataviva.api_url + "/sc/year/?year=2017&" + filter,
        title: dictionary['number_classes'] + ' (2017)',
        value:  'classes'
    });
    Indicator.add({
        url: dataviva.api_url + "/sc/year/?year=2017&" + filter,
        title: dictionary['number_schools'] + ' (2017)',
        value:  'schools'
    });
    Indicator.add({
        url: dataviva.api_url + "/sc/year/?year=2017&" + filter,
        title: dictionary['average_class_size'] + ' (2017)',
        value:  'average_class_size'
    });
    Indicator.add({
        url: dataviva.api_url + "/sc/year/?year=2017&" + filter,
        title: dictionary['average_age'] + ' (2017)',
        value:  'average_age'
    });

    //GENERAL ADD 
    General.add({
        url: dataviva.api_url + '/sc/year/municipality/?order=students&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_municipality_students'],
        label: {
                metadata: true,
                value: 'municipality'
            },
        value: 'students',
    });

    General.add({
        url: dataviva.api_url + '/sc/year/sc_school/?order=students&year=2017&direction=desc&limit=1&' + filter,
        title: dictionary['main_school'],
        label: {
            funct: function(response) {
                var metadata = '';
                $.ajax({
                    url: dataviva.api_url + '/metadata/sc_school/'+response[0]['sc_school'],
                    type: 'GET',
                    async: false,
                    success: function(school){
                        metadata = school['name_' + lang];
                    }
                });
                return metadata;
            }
        },
        value: 'students',
    });
});