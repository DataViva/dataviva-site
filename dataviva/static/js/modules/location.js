$(document).ready(function(){

    var locations = {
        1: "region",
        2: "state",
        4: "mesoregion",
        5: "microregion",
        7: "municipality"
    };

    var idIbge = $('#id_ibge').val();
    var filter = idIbge ? locations[idIbge.length] + '=' + idIbge : '';
    var isMunicipality = idIbge.length == 7;
    var lang = location.pathname.split('/')[1];

    if(isMunicipality) {
    //HEALTH
        General.add({
            url: dataviva.api_url + "cnes_establishment/year/?year=2015&" + filter,
            title:  dictionary['total_of_establishments'],
            label: '',
            value: 'establishments',
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + "cnes_bed/year/?year=2015&" + filter,
            title:  dictionary['total_of_beds'],
            label: '',
            value: 'beds',
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + "cnes_professional/year/?year=2015&" + filter,
            title:  dictionary['total_of_professionals'],
            label: '',
            value: 'professionals',
            prefix: dictionary['total_of_professionals'] + ' ',
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + "cnes_equipment/year/?year=2015&" + filter,
            title: dictionary['total_of_equipments'],
            label: '',
            value: 'equipments',
            prefix: dictionary['total_of_equipments'] + ' ',
            id: 'health'
        });

    } else {
    //HEALTH
        General.add({
            url: dataviva.api_url + 'cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_establishments'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'establishments',
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + 'cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_beds'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'beds',
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + 'cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_professionals'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'professionals',
            prefix: dictionary['total_of_professionals'],
            id: 'health'
        });

        General.add({
            url: dataviva.api_url + 'cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_equipments'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'equipments',
            id: 'health'
        });
    }

    if(!idIbge){
        General.add({
            url: dataviva.api_url + "secex/product_section/?type=export&year=2016&order=value&direction=desc&limit=1&" + filter,
            title:  dictionary['main_product_export'],
            preffix: 'USD',
            label: {
                    metadata: true,
                    value: 'product_section'
                },
            value: 'value',
            id: 'trade'
        });

        General.add({
            url: dataviva.api_url + "secex/product_section/?type=import&year=2016&order=value&direction=desc&limit=1&" + filter,
            title:  dictionary['main_product_import'],
            preffix: 'USD',
            label: {
                    metadata: true,
                    value: 'product_section'
                },
            value: 'value',
            id: 'trade'
        });
    } else {
        General.add({
            url: dataviva.api_url + "secex/product/?type=export&year=2016&order=value&direction=desc&limit=1&" + filter,
            title:  dictionary['main_product_export'],
            preffix: 'USD',
            label: {
                    metadata: true,
                    value: 'product'
                },
            value: 'value',
            id: 'trade'
        });

        General.add({
            url: dataviva.api_url + "secex/product/?type=import&year=2016&order=value&direction=desc&limit=1&" + filter,
            title:  dictionary['main_product_import'],
            preffix: 'USD',
            label: {
                    metadata: true,
                    value: 'product'
                },
            value: 'value',
            id: 'trade'
        });
    }
    //EDUCATION
    General.add({
        url: dataviva.api_url + "hedu/university/?year=2015&order=enrolleds&direction=desc&limit=1&" + filter,
        title:  dictionary['university_higher_enrollments'],
        label: {
                metadata: true,
                value: 'university'
            },
        value: 'enrolleds',
        id: 'education'
    });

    General.add({
        url: dataviva.api_url + "hedu/hedu_course/?year=2015&order=enrolleds&direction=desc&limit=1&" + filter,
        title:  dictionary['course_higher_enrollments'],
        label: {
                metadata: true,
                value: 'hedu_course'
            },
        value: 'enrolleds',
        id: 'education'
    });

    General.add({
        url: dataviva.api_url + "sc/sc_school/?year=2015&order=students&direction=desc&limit=1&" + filter,
        title:  dictionary['school_higher_enrollments'],
        label: {
            funct: function(response) {
                var metadata = '';
                $.ajax({
                    url: dataviva.api_url + 'metadata/sc_school/'+response[0]['sc_school'],
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
        id: 'education'
    });

    General.add({
        url: dataviva.api_url + "sc/sc_course/?year=2015&order=students&direction=desc&limit=1&" + filter,
        title:  dictionary['sc_course_higher_enrollments'],
        label: {
                metadata: true,
                value: 'sc_course'
            },
        value: 'students',
        id: 'education'
    });

    //TRADE


    General.add({
        url: dataviva.api_url + "secex/year/?type=export&year=2016&" + filter,
        title:  dictionary['total_export'],
        preffix: 'USD',
        label: '',
        value: 'value',
        id: 'trade'
    });

    General.add({
        url: dataviva.api_url + "secex/year/?type=import&year=2016&" + filter,
        title:  dictionary['total_import'],
        preffix: 'USD',
        label: '',
        value: 'value',
        id: 'trade'
    });
    if(idIbge){
        General.add({
            url: dataviva.api_url + 'rais/year/industry_class/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_economic_activity'],
            label: {
                    metadata: true,
                    value: 'industry_class'
                },
            value: 'jobs',
            id: 'wage'
        });
        General.add({
            url: dataviva.api_url + 'rais/year/occupation_family/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_occupation'],
            label: {
                    metadata: true,
                    value: 'occupation_family'
                },
            value: 'jobs',
            id: 'wage'
        });
    }
    else{
        General.add({
            url: dataviva.api_url + 'rais/year/industry_section/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_economic_activity'],
            label: {
                    metadata: true,
                    value: 'industry_section'
                },
            value: 'jobs',
            id: 'wage'
        });
        General.add({
            url: dataviva.api_url + 'rais/year/occupation_group/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_occupation'],
            label: {
                    metadata: true,
                    value: 'occupation_group'
                },
            value: 'jobs',
            id: 'wage'
        });
    }


    General.add({
        url: dataviva.api_url + 'rais/year/?year=2014&' + filter,
        preffix: 'R$',
        title: dictionary['average_wage'],
        label: '',
        value: 'average_wage',
        id: 'wage'
    });

    General.add({
        url: dataviva.api_url + 'rais/year/?year=2014&' + filter,
        title: dictionary['total_jobs'],
        label: '',
        value: 'jobs',
        id: 'wage'
    });

//BLUEBOXES ADDS
    //HEALTH
    BlueBox.add({
        url: dataviva.api_url + "cnes_bed/year/?year=2015&" + filter,
        title: dictionary['total_of_beds'],
        label: dictionary['total_of_beds'],
        value: 'beds',
        tab: 'health'
    });

    BlueBox.add({
        url: dataviva.api_url + "cnes_professional/year/?year=2015&" + filter,
        title: dictionary['total_of_professionals'],
        label: dictionary['total_of_professionals'],
        value: 'professionals',
        tab: 'health'
    });

    BlueBox.add({
        url: dataviva.api_url + "cnes_equipment/year/?year=2015&" + filter,
        title: dictionary['total_of_equipments'],
        label: dictionary['total_of_equipments'],
        value: 'equipments',
        tab: 'health'
    });

    BlueBox.add({
        url: dataviva.api_url + "cnes_establishment/year/?year=2015&" + filter,
        title: dictionary['total_of_establishments'],
        label: dictionary['total_of_establishments'],
        value: 'establishments',
        tab: 'health'
    });

    //INTERNATIONAL TRADE
    if(!idIbge){
            BlueBox.add({
                url: dataviva.api_url + "secex/product_section/?type=export&year=2016&order=value&direction=desc&limit=1&" + filter,
                title: dictionary['main_product'],
                subtitle: dictionary['by_export'],
                label:{
                    metadata: true,
                    value: 'product_section'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });

            BlueBox.add({
                url: dataviva.api_url + "secex/product_section/?type=import&year=2016&order=value&direction=desc&limit=1&" + filter,
                title: dictionary['main_product'],
                subtitle: dictionary['by_import'],
                label:{
                    metadata: true,
                    value: 'product_section'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });


    }else{
            BlueBox.add({
                url: dataviva.api_url + "secex/product/?type=export&year=2016&order=value&direction=desc&limit=1&" + filter,
                title: dictionary['main_product'],
                subtitle: dictionary['by_export'],
                label:{
                    metadata: true,
                    value: 'product'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });

            BlueBox.add({
                url: dataviva.api_url + "secex/product/?type=import&year=2016&order=value&direction=desc&limit=1&" + filter,
                title: dictionary['main_product'],
                subtitle: dictionary['by_import'],
                label:{
                    metadata: true,
                    value: 'product'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });

            BlueBox.add({
                url: dataviva.api_url + "secex/country/?year=2016&order=value&direction=desc&limit=1&type=export&" + filter,
                title: dictionary['main_destination'],
                subtitle: dictionary['by_export'],
                label: {
                    metadata: true,
                    value: 'country'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });

            BlueBox.add({
                url: dataviva.api_url + "secex/country/?year=2016&order=value&direction=desc&limit=1&type=import&" + filter,
                title: dictionary['main_origin'],
                subtitle: dictionary['by_import'],
                label: {
                    metadata: true,
                    value: 'country'
                },
                value: 'value',
                prefix: 'USD',
                tab: 'trade-partner'
            });
    }
    BlueBox.add({
        url: dataviva.api_url + "secex/year/?year=2016&type=export&" + filter,
        title: dictionary['total_export'],
        label: dictionary['total_export'],
        value: 'value',
        prefix: 'USD',
        tab: 'trade-partner'
    });

    BlueBox.add({
        url: dataviva.api_url + "secex/year/?year=2016&type=import&" + filter,
        title: dictionary['total_import'],
        label: dictionary['total_import'],
        value: 'value',
        prefix: 'USD',
        tab: 'trade-partner'
    });

    //EDUCATION
    BlueBox.add({
            url: dataviva.api_url + 'hedu/year/university/?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
            title: dictionary['university'],
            subtitle: dictionary['highest_enrolleds'],
            label: {
                metadata: true,
                value: 'university'
            },
            value: 'enrolleds',
            tab: 'education'
    });
    if(idIbge){
        BlueBox.add({
                url: dataviva.api_url + 'hedu/year/hedu_course/?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
                title: dictionary['major'],
                subtitle: dictionary['highest_enrolleds'],
                label: {
                    metadata: true,
                    value: 'hedu_course'
                },
                value: 'enrolleds',
                tab: 'education'
        });
    }else{
        BlueBox.add({
                url: dataviva.api_url + 'hedu/year/hedu_course_field/?order=enrolleds&year=2015&direction=desc&limit=1&' + filter,
                title: dictionary['major'],
                subtitle: dictionary['highest_enrolleds'],
                label: {
                    metadata: true,
                    value: 'hedu_course_field'
                },
                value: 'enrolleds',
                tab: 'education'
        });
    }
    BlueBox.add({
            url: dataviva.api_url + 'sc/year/sc_school/?order=students&year=2015&direction=desc&limit=1&' + filter,
            title: dictionary['school'],
            subtitle: dictionary['highest_enrolleds'],
              label: {
                funct: function(response) {
                    var metadata = '';
                    $.ajax({
                        url: dataviva.api_url + 'metadata/sc_school/'+response[0]['sc_school'],
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
            tab: 'education'
    });
    if(idIbge){
        BlueBox.add({
                url: dataviva.api_url + 'sc/year/sc_course/?order=students&year=2015&direction=desc&limit=1&' + filter,
                title: dictionary['basic_course'],
                subtitle: dictionary['highest_enrolleds'],
                label: {
                    metadata: true,
                    value: 'sc_course'
                },
                value: 'students',
                tab: 'education'
        });
    }else{
        BlueBox.add({
                url: dataviva.api_url + 'sc/year/sc_course_field/?order=students&year=2015&direction=desc&limit=1&' + filter,
                title: dictionary['basic_course'],
                subtitle: dictionary['highest_enrolleds'],
                label: {
                    metadata: true,
                    value: 'sc_course_field'
                },
                value: 'students',
                tab: 'education'
        });
    }

    //WAGE AND JOBS
    if(!idIbge){
        BlueBox.add({
            url: dataviva.api_url + 'rais/year/industry_section/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_economic_activity'],
            subtitle: dictionary['by_jobs'],
            label: {
                metadata: true,
                value: 'industry_section'
            },
            value: 'jobs',
            tab: 'wages'
        });

        BlueBox.add({
            url: dataviva.api_url + 'rais/year/occupation_group/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_occupation'],
            subtitle: dictionary['by_jobs'],
            label: {
                metadata: true,
                value: 'occupation_group'
            },
            value: 'jobs',
            tab: 'wages'
        });
    } else {
        BlueBox.add({
            url: dataviva.api_url + 'rais/year/industry_class/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_economic_activity'],
            subtitle: dictionary['by_jobs'],
            label: {
                metadata: true,
                value: 'industry_class'
            },
            value: 'jobs',
            tab: 'wages'
        });

        BlueBox.add({
            url: dataviva.api_url + 'rais/year/occupation_family/?order=jobs&year=2014&direction=desc&limit=1&' + filter,
            title: dictionary['main_occupation'],
            subtitle: dictionary['by_jobs'],
            label: {
                metadata: true,
                value: 'occupation_family'
            },
            value: 'jobs',
            tab: 'wages'
        });

    }

    BlueBox.add({
        url: dataviva.api_url + 'rais/year/?year=2014&' + filter,
        title: dictionary['avg_wage'],
        prefix: 'R$',
        label: dictionary['avg_wage'],
        value: 'average_wage',
        tab: 'wages'
    });

    BlueBox.add({
        url: dataviva.api_url + 'rais/year/?year=2014&' + filter,
        title: dictionary['wage'],
        prefix: 'R$',
        label: dictionary['wage'],
        value: 'wage',
        tab: 'wages'
    });

    BlueBox.add({
        url: dataviva.api_url + 'rais/year/?year=2014&' + filter,
        title: dictionary['total_jobs'],
        label: dictionary['total_jobs'],
        value: 'jobs',
        tab: 'wages'
    });
});
