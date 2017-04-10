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

    if(isMunicipality) {
        General.add({
            url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filter,
            title:  dictionary['total_of_establishments'],
            label: '',
            value: 'establishments',
            id: 'health'
        });

        General.add({
            url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filter,
            title:  dictionary['total_of_beds'],
            label: '',
            value: 'beds',
            id: 'health'
        });

        General.add({
            url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filter,
            title:  dictionary['total_of_professionals'],
            label: '',
            value: 'professionals',
            prefix: dictionary['total_of_professionals'] + ' ',
            id: 'health'
        });

        General.add({
            url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filter,
            title: dictionary['total_of_equipments'],
            label: '',
            value: 'equipments',
            prefix: dictionary['total_of_equipments'] + ' ',
            id: 'health'
        });
    } else {
        General.add({
            url: 'http://api.staging.dataviva.info/cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_establishments'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'establishments',
            id: 'health'
        });

        General.add({
            url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_beds'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'beds',
            id: 'health'
        });

        General.add({
            url: 'http://api.staging.dataviva.info/cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filter,
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
            url: 'http://api.staging.dataviva.info/cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filter,
            title: dictionary['municipality_with_highest_number_of_equipments'],
            label: {
                metadata: true,
                value: 'municipality'
            },
            value: 'equipments',
            id: 'health'
        });
    }
});
