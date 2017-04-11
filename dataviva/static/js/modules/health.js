$(document).ready(function(){
    var filters = location.search.slice(1);

    if(location.pathname.split('/')[2] == 'health')
        filters = 'establishment=' + location.pathname.split('/')[3];

    if(filters.split('=').indexOf('municipality') == -1){
        // BlueBox.add({
        //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?order=beds&direction=desc&limit=1&' + filters,
        //     title: 'Município com Maior',
        //     subtitle: 'Número de Leitos',
        //     label: {
        //         metadata: true,
        //         value: 'municipality'
        //     },
        //     value: 'beds',
        //     suffix: 'Leitos',
        //     tab: 'beds'
        // });

    }
//GENERAL ADD

//ESTABLISHMENT
    // General.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title:  dictionary['total_of_establishments'],
    //     label: '',
    //     value: 'establishments'
    // });

    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_establishments'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'establishments',
    // });

//BED
    General.add({
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title:  dictionary['total_of_beds'],
        label: '',
        value: 'beds'

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_beds'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'beds'
    // });

//PROFESSIONAL
    General.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title:  dictionary['total_of_professionals'],
        label: '',
        value: 'professionals',
        prefix: dictionary['total_of_professionals'] + ' '

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_professionals'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'professionals',
    //     prefix: 'Total of profissionais'
    // });

//EQUIPMENT
    General.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['total_of_equipments'],
        label: '',
        value: 'equipments',
        prefix: dictionary['total_of_equipments'] + ' '

    });
    // General.add({
    //     url: 'http://api.staging.dataviva.info/cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filters,
    //     title: dictionary['municipality_with_highest_number_of_equipments'],
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'equipments'
    // });
    // ESTABLISHMENTS

    // BlueBox.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title: 'Total de Estabelecimentos',
    //     label: 'Total de Estabelecimentos',
    //     value: 'establishments',
    //     tab: 'establishments'
    // });

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_establishment/municipality/?year=2015&order=establishments&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Estabelecimentos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'establishments',
    //     suffix: 'Estabelecimentos',
    //     tab: 'establishments'
    // });

    // BlueBox.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/unit_type/?year=2015&" + filters,
    //     title: 'Principal Tipo Estabelecimento',
    //     subtitle: 'por Quantidade',
    //     label: {
    //         metadata: true,
    //         value: 'unit_type'
    //     },
    //     value: 'establishments',
    //     tab: 'establishments'
    // });

    // BEDS

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_bed/municipality/?year=2015&order=beds&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Leitos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'beds',
    //     suffix: 'Leitos',
    //     tab: 'beds'
    // });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/cnes_bed/year/bed_type/?year=2015&order=beds&direction=desc&limit=1&' + filters,
        title: dictionary['main_bed_type'],
        subtitle: dictionary['by_quantity'],
        label: {
            metadata: true,
            value: 'bed_type'
        },
        value: 'beds',
        tab: 'beds'
    });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title: dictionary['total_of_beds'],
        label: dictionary['total_of_beds'],
        value: 'beds',
        tab: 'beds'
    });

    // PROFESSIONALS

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_professional/municipality/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Profissionais',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'professionals',
    //     suffix: 'Profissionais',
    //     tab: 'professionals'
    // });

    BlueBox.add({
        url: 'http://api.staging.dataviva.info/cnes_professional/year/occupation_family/?year=2015&order=professionals&direction=desc&limit=1&' + filters,
        title: dictionary['main_occupation'],
        subtitle: dictionary['by_jobs'],
        label: {
            metadata: true,
            value: 'occupation_family'
        },
        value: 'professionals',
        tab: 'professionals'
    });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title: dictionary['total_of_professionals'],
        label: dictionary['total_of_professionals'],
        value: 'professionals',
        tab: 'professionals'
    });

    // EQUIPMENTS

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['total_of_equipments'],
        label: dictionary['total_of_equipments'],
        value: 'equipments',
        tab: 'equipments'
    });

    // BlueBox.add({
    //     url: 'http://api.staging.dataviva.info/cnes_equipment/municipality/?year=2015&order=equipments&direction=desc&limit=1&' + filters,
    //     title: 'Município com Maior',
    //     subtitle: 'Número de Equipamentos',
    //     label: {
    //         metadata: true,
    //         value: 'municipality'
    //     },
    //     value: 'equipments',
    //     suffix: 'Equipamentos',
    //     tab: 'equipments'
    // });

    BlueBox.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/equipment_type/?year=2015&" + filters,
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
        url: "http://api.staging.dataviva.info/cnes_bed/year/?year=2015&" + filters,
        title: dictionary['number_beds'],
        value:  'beds'
    });

    //EQUIPAMENTOS
    Indicator.add({
        url: "http://api.staging.dataviva.info/cnes_equipment/year/?year=2015&" + filters,
        title: dictionary['number_equipments'],
        value:  'equipments'
    });

    //PROFISSIONAIS
    Indicator.add({
        url: "http://api.staging.dataviva.info/cnes_professional/year/?year=2015&" + filters,
        title: dictionary['number_professionals'],
        value:  'professionals'
    });

    //ESTABELECIMENTOS
    // Indicator.add({
    //     url: "http://api.staging.dataviva.info/cnes_establishment/year/?year=2015&" + filters,
    //     title: dictionary.number_establishments,
    //     value:  'establishments'
    // });
    //


})
