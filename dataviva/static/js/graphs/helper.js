var lang = document.documentElement.lang,
    API_DOMAIN = 'http://api.staging.dataviva.info';

var DICT = {
    'secex': {
        'item_id': {
            'municipality': 'ibge_id',
            'product': 'hs_id',
            'country': 'wld_id'
        },
        'kg': {
            'export': 'export_kg',
            'import': 'import_kg'
        },
        'value': {
            'export': 'exports',
            'import': 'imports'
        },
        'value_per_kg': {
            'export': 'export_val_kg',
            'import': 'import_val_kg'
        }
    },
    'rais': {
        'item_id': {
            'industry_class': 'cnae_id',
            'municipality': 'ibge_id',
            'occupation_family': 'cbo_id'
        },
        'jobs': 'total_jobs'
    },
    'cnes_establishment': {
        'item_id': {
            'municipality': 'ibge_id',
            'state': 'ibge_id'
        }
    },
    'cnes_equipment': {
        'item_id': {
            'equipment_type': 'id'
        }
    },
    'cnes_bed': {
        'item_id': {
            'bed_type': 'id'
        }
    },
    'cnes_professional': {
        'item_id': {
            'municipality': 'ibge_id'
        }
    }
};

var DEPTHS = {
    'secex': {
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'municipality'],
        'product': ['product_section', 'product'],
        'country': ['continent', 'country'],
        'port': ['port']
    },
    'rais': {
        'industry_class': ['industry_section', 'industry_division', 'industry_class'],
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'municipality'],
        'occupation_family': ['occupation_group', 'occupation_family']
    },
    'cnes_establishment': {
       'municipality': ['health_region', 'unit_type', 'provider_type'],
       'provider_type': ['tax_withholding', 'hierarchy_level', 'administrative_sphere'],
       'unit_type': ['tax_withholding', 'hierarchy_level', 'administrative_sphere'],
       'administrative_sphere': ['administrative_sphere']
   },
   'cnes_equipment': {
        'equipment_type': ['health_region', 'unit_type'],
        'municipality': ['health_region', 'equipment_type', 'unit_type']
   },
    'cnes_bed': {
        'municipality': ['health_region', 'bed_type', 'bed_type_per_specialty'],
        'unit_type': ['health_region', 'bed_type', 'bed_type_per_specialty'],
        'provider_type': ['health_region', 'bed_type', 'bed_type_per_specialty'],
        'bed_type': ['health_region', 'bed_type_per_specialty']
   },
   'cnes_professional': {
        'municipality': ['health_region', 'municipality'],
        'professional_link': ['health_region', 'occupation_family', 'sus_healthcare_professional']
   }
};

var SIZES = {
    'secex': {
        'municipality': ['value', 'kg'],
        'product': ['value', 'kg'],
        'country': ['value', 'kg'],
        'port': ['value', 'kg']
    },
    'rais': {
        'industry_class': ['jobs', 'wage', 'establishment_count'],
        'municipality': ['jobs', 'wage', 'establishment_count'],
        'occupation_family': ['jobs', 'wage']
    },
    'cnes_establishment': {
        'municipality': ['establishments'],
        'health_region': ['establishments'],
        'state': ['establishments'],
        'provider_type': ['establishments'],
        'unit_type': ['establishments'],
        'administrative_sphere': ['establishments']
    },
    'cnes_equipment': {
        'municipality': ['equipment_quantity', 'equipment_quantity_in_use'],
        'equipment_type': ['equipment_quantity', 'equipment_quantity_in_use']
    },
    'cnes_bed': {
        'bed_type': ['beds', 'number_sus_bed', 'number_non_sus_bed', 'number_existing_contract'],
        'municipality': ['beds', 'number_sus_bed', 'number_non_sus_bed', 'number_existing_contract'],
        'unit_type': ['beds', 'number_sus_bed', 'number_non_sus_bed', 'number_existing_contract'],
        'provider_type': ['beds', 'number_sus_bed', 'number_non_sus_bed', 'number_existing_contract']
   },
    'cnes_professional': {
        'municipality': ['professionals'],
        'unit_type': ['professionals'],
        'occupation_family': ['professionals', 'other_hours_worked', 'hospital_hour', 'ambulatory_hour']
    }
};

var COLORS = {
    'secex': {},
    'rais': {},
    'cnes_establishment': {
        'municipality': [],
        'provider_type': ['administrative_sphere', 'tax_withholding', 'hierarchy_level'],
        'unit_type': ['administrative_sphere', 'tax_withholding', 'hierarchy_level'],
        'administrative_sphere': []
        // 'administrative_sphere': ['ambulatory_care_facilities', 'emergency_facilities', 'neonatal_unit_facilities', 'obstetrical_center_facilities', 'surgery_center_facilities', 'selective_waste_collection']
    }
};

var FILTERS = {
    'secex': {},
    'rais': {},
    'cnes_establishment': {
        'municipality': [],
        'administrative_sphere': ['sus_bond'],
        'provider_type': [],
        'unit_type': [],
    },
    'cnes_equipment': {},
    'cnes_professional': {},
    'cnes_bed': {}
};

var DIMENSION_COLOR = {
    'provider_type': {
        '30': '#4575B4',
        '40': '#74ADD1',
        '50': '#ABD9E9',
        '61': '#E0F3F8',
        '80': '#F46D43',
        '20': '#D73027',
        '22': '#FDAE61',
        '60': '#FEE090',
        '99': '#FFFFBF'
    }
};

var BASIC_VALUES = {
    'secex': ['value', 'kg'],
    'rais': ['jobs', 'wage', 'average_wage', 'establishment_count', 'average_establishment_size'],
    'cnes_establishment': ['establishments'],
    'cnes_equipment': ['equipment_quantity', 'equipment_quantity_in_use'],
    'cnes_bed': ['beds'],
    'cnes_professional': ['professionals', 'other_hours_worked', 'hospital_hour', 'ambulatory_hour']
};

if (document.getElementById('rings'))
    BASIC_VALUES['secex'] = ['exports_value', 'exports_weight', 'imports_value', 'imports_weight']

var CALC_BASIC_VALUES = {
    'secex': {
        'exports_per_weight': function(dataItem) {
            return getUrlArgs()['type'] == 'export' ? dataItem['value'] / dataItem['kg'] : undefined;
        },
        'imports_per_weight': function(dataItem) {
            return getUrlArgs()['type'] == 'import' ? dataItem['value'] / dataItem['kg'] : undefined;
        }
    },
    'rais': {},
    'cnes_establishment': {},
    'cnes_equipment': {},
    'cnes_bed': {},
    'cnes_professional': {}
};

var HAS_ICONS = ['continent', 'industry_section', 'product_section', 'occupation_group'];

// Temporarily translates text until dictionary is updated
dictionary['state'] = lang == 'en' ? 'State' : 'Estado';
dictionary['states'] = lang == 'en' ? 'States' : 'Estados';
dictionary['municipality'] = lang == 'en' ? 'Municipality' : 'Município';
dictionary['municipalities'] = lang == 'en' ? 'Municipalities' : 'Municípios';
dictionary['product_section'] = lang == 'en' ? 'Section' : 'Seção';
dictionary['product'] = lang == 'en' ? 'Product' : 'Produto';
dictionary['data_provided_by'] = lang == 'en' ? 'Data provided by' : 'Dados fornecidos por';
dictionary['by'] = lang == 'en' ? 'by' : 'por';
dictionary['that trade'] = lang == 'en' ? 'that trade' : 'que comercializam';
dictionary['of'] = lang == 'en' ? 'of' : 'de';
dictionary['number of'] = lang == 'en' ? 'number of' : 'número de';
dictionary['port'] = lang == 'en' ? 'Port' : 'Porto';
dictionary['country'] = lang == 'en' ? 'Country' : 'País';
dictionary['countries'] = lang == 'en' ? 'Countries' : 'Países';
dictionary['continent'] = lang == 'en' ? 'Continent' : 'Continente';
dictionary['continents'] = lang == 'en' ? 'Continents' : 'Continentes';
dictionary['mesoregion'] = lang == 'en' ? 'Mesoregion' : 'Mesorregião';
dictionary['mesoregions'] = lang == 'en' ? 'Mesoregions' : 'Mesorregiões';
dictionary['microregion'] = lang == 'en' ? 'Microregion' : 'Microrregião';
dictionary['microregions'] = lang == 'en' ? 'Microregions' : 'Microrregiões';
dictionary['region'] = lang == 'en' ? 'Region' : 'Região';
dictionary['regions'] = lang == 'en' ? 'Regions' : 'Regiões';
dictionary['basic_values'] = lang == 'en' ? 'Basic Values' : 'Valores Básicos';
dictionary['market_share'] = lang == 'en' ? 'Market Share' : 'Participação de Mercado';
dictionary['item_id'] = 'ID';
dictionary['ibge_id'] = lang == 'en' ? 'IBGE ID' : 'ID IBGE';
dictionary['per'] = lang == 'en' ? 'per' : 'por';
dictionary['exports_value'] = lang == 'en' ? 'Export Value' : 'Valor das Exportações';
dictionary['imports_value'] = lang == 'en' ? 'Import Value' : 'Valor das Importações';
dictionary['exports_weight'] = lang == 'en' ? 'Export Weight' : 'Peso das Exportações';
dictionary['imports_weight'] = lang == 'en' ? 'Import Weight' : 'Peso das Importações';
dictionary['imports_per_weight'] = lang == 'en' ? 'Imports per kg' : 'Importações por peso';
dictionary['exports_per_weight'] = lang == 'en' ? 'Exports per kg' : 'Exportações por peso';
dictionary['industry_section'] = lang == 'en' ? 'Section' : 'Seção';
dictionary['industry_division'] = lang == 'en' ? 'Division' : 'Divisão';
dictionary['establishment_count'] = lang == 'en' ? 'Total Establishments' : 'Total de Estabelecimentos';
dictionary['wage'] = lang == 'en' ? 'Total Monthly Wages' : 'Renda Mensal Total';
dictionary['average_wage'] = lang == 'en' ? 'Average Monthly Wages' : 'Renda Mensal Média';
dictionary['industry_class'] = lang == 'en' ? 'Class' : 'Classe';
dictionary['total_jobs'] = lang == 'en' ? 'Total Jobs' : 'Total de Empregos';
dictionary['average_establishment_size'] = lang == 'en' ? 'Jobs per Establishment' : 'Empregos por Estabelecimento';
dictionary['occupation_family'] = lang == 'en' ? 'Family' : 'Família';
dictionary['occupation_group'] = lang == 'en' ? 'Main Group' : 'Grande Grupo';
dictionary['establishments'] = lang == 'en' ? 'Total Establishments' : 'Total de Estabelecimentos';
dictionary['Creating URL'] = lang == 'en' ? 'Creating URL' : 'Criando URL';
dictionary['drawer_group'] = lang == 'en' ? 'Group' : 'Agrupar';
dictionary['yes'] = lang == 'en' ? 'Yes' : 'Sim';
dictionary['no'] = lang == 'en' ? 'No' : 'Não';
dictionary['drawer_filter'] = lang == 'en' ? 'Filter' : 'Filtrar';
dictionary['Filter by'] = lang == 'en' ? 'Filter by' : 'Filtrar por';
dictionary['kg'] = 'KG';
dictionary['id'] = 'ID';

// CNES
dictionary['health_region'] = lang == 'en' ? 'Health region' : 'Região de Saúde';
dictionary['unit_type'] = lang == 'en' ? 'Unit Type' : 'Tipo de Unidade';

// CNES BEDS
dictionary['bed_type'] = lang == 'en' ? 'Bed Type' : 'Tipo de Leito';
dictionary['number_existing_bed'] = lang == 'en' ? 'Number of Existing Beds' : 'Quantidade de Leitos Existentes';
dictionary['bed_type_per_specialty'] = lang == 'en' ? 'Bed Type Per Specialty' : 'Tipo de Especialidade do Leito';
dictionary['cnes_bed'] = lang == 'en' ? 'Datasus' : 'Datasus';
dictionary['beds'] = lang == 'en' ? 'Total Beds' : 'Total de Leitos';
dictionary['number_sus_bed'] = lang == 'en' ? 'SUS Beds' : 'Leitos SUS';
dictionary['number_non_sus_bed'] = lang == 'en' ? 'Non SUS Beds' : 'Leitos não SUS';
dictionary['number_existing_contract'] = lang == 'en' ? 'Existing Contracts Number' : 'Quantidade de Contratos Existentes';

// CNES PROFESSIONALS
dictionary['sus_healthcare_professional'] = lang == 'en' ? 'SUS Professionals' : 'Profissionais do SUS';
dictionary['professional_link'] = lang == 'en' ? 'Link' : 'Vinculação';
dictionary['cnes_professional'] = lang == 'en' ? 'datasus' : 'datasus';
dictionary['professionals'] = lang == 'en' ? 'Total Professionals' : 'Total de Profissionais';
dictionary['other_hours_worked'] = lang == 'en' ? 'Other Hours Worked' : 'Outras Horas Trabalhadas';
dictionary['hospital_hour'] = lang == 'en' ? 'Hospital Hours' : 'Horas Hospitalares';
dictionary['ambulatory_hour'] = lang == 'en' ? 'Ambulary Hours' : 'Horas Ambulatoriais';

// CNES ESTABLISHMENTS
dictionary['sus_bond'] = lang == 'en' ? 'SUS Bond' : 'Vínculo com o SUS';
dictionary['provider_type'] = lang == 'en' ? 'Provider Type' : 'Tipo de Prestador';
dictionary['ambulatory_care_facility'] = lang == 'en' ? 'Ambulatory Care Facility' : 'Instalações Físicas de Atendimento ambulatorial';
dictionary['administrative_sphere'] = lang == 'en' ? 'Administrative Sphere' : 'Esfera Administrativa';
dictionary['tax_withholding'] = lang == 'en' ? 'Withholding Tax' : 'Retenção Tributária';
dictionary['emergency_facility'] = lang == 'en' ? 'Emergency Facilities' : 'Instalações Físicas de Urgência e Emergência';
dictionary['neonatal_unit_facility'] = lang == 'en' ? 'Neonatal Unit Facilities' : 'Instalações de Unidade Neonatal';
dictionary['obstetrical_center_facility'] = lang == 'en' ? 'Obstetrical Center Facilities' : 'Instalação Fisica de Centro Obstétrico ';
dictionary['surgery_center_facility'] = lang == 'en' ? 'Surgery Center Facilities' : 'Instalação Fisica de Centro Cirúrgico';
dictionary['selective_waste_collection'] = lang == 'en' ? 'Selective Waste Collection' : 'Coleta seletiva de rejeitos';
dictionary['hospital_attention'] = lang == 'en' ? 'Hospital Attention' : 'Nível de Atenção Hospitalar';
dictionary['ambulatory_attention'] = lang == 'en' ? 'Ambulatory Attention' : 'Nível de Atenção Ambulatorial';
dictionary['hierarchy_level'] = lang == 'en' ? 'Hierarchy Level' : 'Nível de Hierarquia';
dictionary['cnes_establishment'] = lang == 'en' ? 'datasus' : 'datasus';
dictionary['hospital_attention'] = lang == 'en' ? 'Level Of Hospital Care' : 'Nível de Atenção Hospitalar';
dictionary['ambulatory_attention'] = lang == 'en' ? 'Level Of Ambulatory Care' : 'Nível de Atenção Ambulatorial';
dictionary['ambulatory_care_facilities'] = lang == 'en' ? 'Physical Facilities Of Outpatient Care' : 'Instalações Físicas de Atendimento Ambulatorial';
dictionary['hospital_care'] = lang == 'en' ? 'Hospital Care' : 'Atendimento Hospitalar';
dictionary['dependency_level'] = lang == 'en' ? 'Dependency Level' : 'Nível de Dependência';

// CNES EQUIPMENTS
dictionary['equipment_type'] = lang == 'en' ? 'Equipment Type' : 'Tipo de Equipamento';
dictionary['equipment_code'] = lang == 'en' ? 'Equipment Code' : 'Código de Equipamento';
dictionary['equipments'] = lang == 'en' ? 'Equipments' : 'Equipamentos';
dictionary['equipment_quantity'] = lang == 'en' ? 'Equipment Quantity' : 'Quantidade Existente';
dictionary['equipment_quantity_in_use'] = lang == 'en' ? 'Equipment quantity in use' : 'Quantidade existente em uso';
dictionary['cnes_equipment'] = lang == 'en' ? 'datasus' : 'datasus';
dictionary['sus_availability_indicator'] = lang == 'en' ? 'Sus Availability Indicator' : 'Indicador de Disponibilidade para o SUS';

var PLURAL = {
    'municipality': dictionary['municipalities'],
    'state': dictionary['states'],
    'microregion': dictionary['microregions'],
    'mesoregion': dictionary['mesoregions'],
    'region': dictionary['regions'],
    'country': dictionary['countries'],
    'product': dictionary['products'],
    'industry_class': dictionary['industries'],
    'industry_section': dictionary['industries'],
    'industry_division': dictionary['industries'],
    'industry_division': dictionary['industries'],
    'occupation_group': dictionary['occupations'],
    'occupation_family': dictionary['occupations']
};

var titleBuilder = function(title, subtitle, attrs, dataset, filters, yearRange) {
    var formatYearRange = function() {
        if (yearRange[0] && yearRange[1])
            return '(' + yearRange[0] + '-' + yearRange[1] + ')';
        if (yearRange[1])
            return '(' + yearRange[1] + ')';
    };

    if (yearRange[0] || yearRange[1])
        title += ' ' + formatYearRange();

    for (attr in attrs) {
        title = title.replace('<' + attr + '>', PLURAL[attrs[attr]] || dictionary[attrs[attr]]);
    }
    title = title.charAt(0).toUpperCase() + title.slice(1);

    return {'title': title, 'subtitle': subtitle};
};

dictionary['time-resolution'] =  lang == 'en' ? 'Time Resolution' : 'Resolução temporal';
dictionary['Order'] =  lang == 'en' ? 'Order' : 'Ordem';
dictionary['sort'] =  lang == 'en' ? 'Sort' : 'Ordenar';
dictionary['market-share'] =  lang == 'en' ? 'Market Share' : 'Particiação de Mercado';
dictionary['y-axis'] = lang == 'en' ? 'Y Axis' : 'Eixo Y';
dictionary['desc'] = lang == 'en' ? 'Descending' : 'Descendente';
dictionary['asc'] = lang == 'en' ? 'Ascending' : 'Ascendente';
dictionary['value'] = lang == 'en' ? 'Value' : 'Valor';
dictionary['name'] = lang == 'en' ? 'Name' : 'Nome';
dictionary['unknown-region'] = lang == 'en' ? 'Unknown Region' : 'Região Desconhecida';

var getUrlArgs = function() {
    var args = {};
    if (window.location.search) {
        window.location.search.split('?')[1].split('&').forEach(function(arg) {
            args[arg.split('=')[0]] = arg.split('=')[1];
        });
    }
    return args;
};

var formatHelper = function() {
    var args = getUrlArgs();

    return {
        'text': function(text, key) {
            switch (text) {
                case 'item_id':
                    return dictionary[DICT[dataset][text][squares]] || dictionary[text];
                case 'value':
                case 'kg':
                case 'value_per_kg':
                    return dictionary[DICT[dataset][text][args['type']]];
                case 'jobs':
                    return dictionary[DICT[dataset][text]];
                case 'primary connections':
                    return text.replace(/\w\S*/g, function(txt) {
                        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                    })
                default:
                if ([dictionary['number_sus_bed'], dictionary['number_non_sus_bed'], dictionary['sus_healthcare_professional'], 
                    dictionary['sus_bond'], dictionary['sus_availability_indicator']].indexOf(text) >= 0)
                    return text;
                return dictionary[text] || text.replace(/\w\S*/g, function(txt) {
                    return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                });
            };

        },
        'number': function(value, opts) {
            var result;

            if (value.toString().split('.')[0].length > 3) {

                var symbol = d3.formatPrefix(value).symbol;
                symbol = symbol.replace('G', 'B');

                value = d3.formatPrefix(value).scale(value);
                value = parseFloat(d3.format('.3g')(value));

                if (symbol && lang === 'pt') {
                    var digit = parseFloat(value.toString().split('.')[0]);
                    switch (symbol) {
                        case 'T':
                            symbol = digit < 2 ? ' Trilh\u00e3o' : ' Trilh\u00f5es';
                            break;
                        case 'B':
                            symbol = digit < 2 ? ' Bilh\u00e3o' : ' Bilh\u00f5es';
                            break;
                        case 'M':
                            symbol = digit < 2 ? ' Milh\u00e3o' : ' Milh\u00f5es';
                            break;
                        case 'k':
                            symbol = ' Mil';
                    }
                }

                result = value + symbol;
            }

            if (!result) {
                result = d3.round(value, 3);
            }

            if (result > 0 && result < 1) {
                result = d3.round(result, 3);
            }

            switch (opts.key) {
                case 'share':
                    result = d3.round(value, 1) + '%';
                    break;
                case 'value':
                case 'imports_per_weight':
                case 'exports_per_weight':
                    result = '$' + result + ' USD';
                    break;
                case 'kg':
                    result += ' kg';
                    break;
                case 'average_wage':
                case 'wage':
                    result = '$' + result + ' BRL';
                    break;
                case 'jobs_per_establishments':
                    result = d3.round(value, 0)
                    break;
            };

            if (result && lang == 'pt') {
                var n = result.toString().split('.')
                n[0] = n[0].replace(',', '.')
                result = n.join(',')
            }

            return result || value;
        }
    }
};
