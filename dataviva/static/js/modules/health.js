$(document).ready(function(){
    var establishment = location.href.split('/')[5];
    var filters = '&year=2015&establishment=' + establishment;

    // GENERAL ADD

    General.add({
        url: dataviva.api_url + "cnes_bed/year?" + filters,
        title:  dictionary['total_of_beds'],
        label: '',
        value: 'beds'
    });

    General.add({
        url: dataviva.api_url + 'cnes_bed/year/bed_type/?year=2015&order=beds&direction=desc&limit=1&' + filters,
        title: dictionary['main_bed_type'],
        label: {
            metadata: true,
            value: 'bed_type'
        },
        value: 'beds'
    });

    General.add({
        url: dataviva.api_url + "cnes_professional/year/?" + filters,
        title:  dictionary['total_of_professionals'],
        label: '',
        value: 'professionals',
    });

    General.add({
        url: dataviva.api_url + 'cnes_professional/year/occupation_family/?order=professionals&direction=desc&limit=1' + filters,
        title: dictionary['main_occupation'],
        label: {
            metadata: true,
            value: 'occupation_family'
        },
        value: 'professionals',
    });

    General.add({
        url: dataviva.api_url + "cnes_equipment/year/?" + filters,
        title: dictionary['total_of_equipments'],
        label: '',
        value: 'equipments',
    });

    General.add({
        url: dataviva.api_url + "cnes_equipment/equipment_type/?year=2015&" + filters,
        title: dictionary['main_equipment_type'],
        label: {
            metadata: true,
            value: 'equipment_type'
        },
        value: 'equipments'
    });

    // BLUEBOX ADD
  
    // BEDS
    BlueBox.add({
        url: dataviva.api_url + "cnes_bed/year/?" + filters,
        title: dictionary['total_of_beds'],
        label: dictionary['total_of_beds'],
        value: 'beds',
        tab: 'beds'
    });

    BlueBox.add({
        url: dataviva.api_url + 'cnes_bed/year/bed_type/?order=beds&direction=desc&limit=1&' + filters,
        title: dictionary['main_bed_type'],
        subtitle: dictionary['by_quantity'],
        label: {
            metadata: true,
            value: 'bed_type'
        },
        value: 'beds',
        tab: 'beds'
    });


    // PROFESSIONALS
    BlueBox.add({
        url: dataviva.api_url + "cnes_professional/year/?" + filters,
        title: dictionary['total_of_professionals'],
        label: dictionary['total_of_professionals'],
        value: 'professionals',
        tab: 'professionals'
    });

    BlueBox.add({
        url: dataviva.api_url + 'cnes_professional/year/occupation_family/?order=professionals&direction=desc&limit=1&' + filters,
        title: dictionary['main_occupation'],
        subtitle: dictionary['by_jobs'],
        label: {
            metadata: true,
            value: 'occupation_family'
        },
        value: 'professionals',
        tab: 'professionals'
    });


    // EQUIPMENTS
    BlueBox.add({
        url: dataviva.api_url + "cnes_equipment/year/?" + filters,
        title: dictionary['total_of_equipments'],
        label: dictionary['total_of_equipments'],
        value: 'equipments',
        tab: 'equipments'
    });

    BlueBox.add({
        url: dataviva.api_url + "cnes_equipment/equipment_type/?" + filters,
        title: dictionary['main_equipment_type'],
        subtitle: dictionary['by_quantity'],
        label: {
            metadata: true,
            value: 'equipment_type'
        },
        value: 'equipments',
        suffix: dictionary['equipments'],
        tab: 'equipments'
    });


    //INDICATOR ADD

    //LEITOS
    Indicator.add({
        url: dataviva.api_url + "cnes_bed/year/?" + filters,
        title: dictionary['number_beds'],
        value:  'beds'
    });

    //EQUIPAMENTOS
    Indicator.add({
        url: dataviva.api_url + "cnes_equipment/year/?" + filters,
        title: dictionary['number_equipments'],
        value:  'equipments'
    });

    //PROFISSIONAIS
    Indicator.add({
        url: dataviva.api_url + "cnes_professional/year/?" + filters,
        title: dictionary['number_professionals'],
        value:  'professionals'
    });
})
