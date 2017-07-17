$(document).ready(function(){

    var universityFilter;

    var university = location.pathname.split('/')[3];
    universityFilter = 'university=' + university;
    filter = [universityFilter].join('&');

    //BLUEBOXES ADD
    BlueBox.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course'],
        subtitle: dictionary['by_number_enrolled'],
        label: {
            metadata: true,
            value: 'hedu_course'
        },
        value: 'enrolleds',
        tab: 'enrollments'
    });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=entrants&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course'],
        subtitle: dictionary['by_number_entrants'],
        label: {
            metadata: true,
            value: 'hedu_course'
        },
        value: 'entrants',
        tab: 'enrollments'
    });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=graduates&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course'],
        subtitle: dictionary['by_number_graduates'],
        label: {
            metadata: true,
            value: 'hedu_course'
        },
        value: 'graduates',
        tab: 'enrollments'
    });

    //INDICATORS ADD
    Indicator.add({
        url: "http://api.staging.dataviva.info/hedu/year/?count=enrollments&year=2015&" + filter,
        title: dictionary['number_enrolleds'] + ' (2015)',
        value:  'enrolleds'
    });

    Indicator.add({
        url: "http://api.staging.dataviva.info/hedu/year/?count=enrollments&year=2015&" + filter,
        title: dictionary['number_entrants'] + ' (2015)',
        value:  'entrants'
    });

    Indicator.add({
        url: "http://api.staging.dataviva.info/hedu/year/?count=enrollments&year=2015&" + filter,
        title: dictionary['number_graduates'] + ' (2015)',
        value:  'graduates'
    });

    //GENERAL ADD
    General.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course_enrolleds'],
        label: {
                metadata: true,
                value: 'hedu_course'
            },
        value: 'enrolleds',
        id: 'enrolleds',
    });

    General.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=entrants&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course_entrants'],
        label: {
                metadata: true,
                value: 'hedu_course'
            },
        value: 'entrants',
        id: 'enrolleds',
    });

    General.add({
        url: 'http://api.staging.dataviva.info/hedu/year/hedu_course/?order=graduates&year=2015&direction=desc&limit=1&' + filter,
        title: dictionary['main_course_graduates'],
        label: {
                metadata: true,
                value: 'hedu_course'
            },
        value: 'graduates',
        id: 'enrolleds',
    });
});