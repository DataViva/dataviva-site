var API_DOMAIN = 'http://api.staging.dataviva.info';

var ID_LABELS = {
    'municipality': 'ibge_id',
    'state': 'ibge_id',
    'region': 'ibge_id',
    'mesoregion': 'ibge_id',
    'microregion': 'ibge_id',
    'health_region': 'id',
    'product': 'hs_id',
    'product_chapter': 'hs_id',
    'product_section': 'hs_id',
    'country': 'wld_id',
    'continent': 'wld_id',
    'unit_type': 'id',
    'provider_type': 'id',
    'occupation_family': 'cbo_id',
    'occupation_group': 'cbo_id',
    'equipment_type': 'id',
    'equipment_code': 'id',
    'industry_class': 'cnae_id',
    'industry_section': 'cnae_id',
    'industry_division': 'cnae_id'
};

var DICT = {
    'secex': {
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
        'jobs': 'total_jobs'
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
       'municipality': ['region', 'state', 'mesoregion', 'microregion', 'health_region', 'municipality'],
       'unit_type': ['provider_type', 'unit_type'],
   },
   'cnes_equipment': {
        'equipment_type': ['health_region', 'equipment_type', 'unit_type', 'equipment_code', 'equipment_type'],
        'municipality': ['health_region', 'equipment_type', 'equipment_code', 'unit_type'],
        'unit_type': ['health_region', 'equipment_type', 'equipment_code'],
        'equipment_code': ['equipment_type', 'equipment_code']
   },
    'cnes_bed': {
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'health_region', 'municipality'],
        'unit_type': ['provider_type', 'unit_type'],
        'bed_type': ['health_region', 'bed_type_per_specialty']
   },
   'cnes_professional': {
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'health_region', 'municipality']
   },
   'hedu': {
        'hedu_course': ['hedu_course_field', 'hedu_course'],
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'municipality']
   },
   'sc': {
        'sc_course': ['sc_course_field' , 'sc_course'],
        'municipality': ['region', 'state', 'mesoregion', 'microregion', 'municipality']
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
        'bed_type': ['beds', 'number_sus_bed', 'number_non_sus_bed'],
        'municipality': ['beds', 'number_sus_bed', 'number_non_sus_bed'],
        'unit_type': ['beds', 'number_sus_bed', 'number_non_sus_bed'],
        'provider_type': ['beds', 'number_sus_bed', 'number_non_sus_bed', 'number_existing_contract']
   },
    'cnes_professional': {
        'municipality': ['professionals'],
        'unit_type': ['professionals'],
        'occupation_family': ['professionals', 'other_hours_worked', 'hospital_hour', 'ambulatory_hour']
    },
    'hedu': {
        'hedu_course': ['graduates', 'entrants'],
        'municipality': ['enrolled','graduates', 'entrants']
   },
    'sc': {
        'sc_course': ['students']
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

var COLORS = {
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
    },
    'continent': {
        'as': '#CC2A21',
        'af': '#FEC932',
        'eu': '#823783',
        'na': '#080C79',
        'oc': '#E98319',
        'sa': '#199C51'
    },
    'region': {
        '1': '#00994C',
        '2': '#101070',
        '3': '#C40008',
        '4': '#A9D046',
        '5': '#F3E718'
    },
    'product_section': {
        '01': '#FFE999',
        '02': '#FFC41C',
        '03': '#E0902F',
        '04': '#D1FF00',
        '05': '#330000',
        '06': '#E377C2',
        '07': '#F7B6D2',
        '08': '#98DF8A',
        '09': '#B00000',
        '10': '#B7834B',
        '11': '#105B10',
        '12': '#3AB11A',
        '13': '#D66011',
        '14': '#752277',
        '15': '#5E1F05',
        '16': '#17BCEF',
        '17': '#9EDAE5',
        '18': '#AA1F61',
        '19': '#A4BD99',
        '20': '#7F7F7F',
        '21': '#93789E',
        '22': '#C7C7C7'
    },
    'type': {
        'export': '#0B1097',
        'import': '#AF1F24',
    },
    'occupation_group': {
        '0': '#A4BD99',
        '1': '#752277',
        '2': '#CC0000',
        '3': '#D66011',
        '4': '#B7834B',
        '5': '#17BCEF',
        '6': '#105B10',
        '7': '#9EDAE5',
        '8': '#FFC41C',
        '9': '#581F05',
        'X': '#C7C7C7'
    },
    'industry_section': {
        'a': '#105B10',
        'b': '#330000',
        'c': '#5E1F05',
        'd': '#e377c2',
        'e': '#2F2F6D',
        'f': '#E87600',
        'g': '#17bcef',
        'h': '#9edae5',
        'i': '#FFC41C',
        'j': '#57D200',
        'k': '#408e60',
        'l': '#a4bd99',
        'm': '#cc0000',
        'n': '#b7834b',
        'o': '#752277',
        'p': '#d66011',
        'q': '#800000',
        'r': '#93789e',
        's': '#c7c7c7',
        't': '#f7b6d2',
        'u': '#4C4C4C',
        'x': '#C7C7C7'
    },
    'shift': {
        '-1': '#ccc',
        1: '#F7B6D2',
        2: '#FFC41C',
        3: '#2F2F6D',
        4: '#105B10'
    }
};

var BASIC_VALUES = {
    'secex': ['value', 'kg'],
    'sc': ['students'],
    'hedu': ['enrolled', 'entrants', 'graduates'],
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
            return getUrlArgs()['type'] == 'export' || dataItem['type'] == 'export' ? dataItem['value'] / dataItem['kg'] : undefined;
        },
        'imports_per_weight': function(dataItem) {
            return getUrlArgs()['type'] == 'import' || dataItem['type'] == 'import' ? dataItem['value'] / dataItem['kg'] : undefined;
        }
    },
    'sc': {},
    'hedu': {},
    'rais': {},
    'cnes_establishment': {},
    'cnes_equipment': {},
    'cnes_bed': {},
    'cnes_professional': {}
};

var HAS_ICONS = ['continent', 'industry_section', 'product_section', 'occupation_group', 'hedu_course_field', 'shift'];
var NEEDS_CASTING = ['wage', 'average_wage', 'enrolled', 'entrants', 'graduates'];

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
        title = title.replace('<' + attr + '>', dictionary['plural_' + attrs[attr]] || dictionary[attrs[attr]]);
    }
    title = title.charAt(0).toUpperCase() + title.slice(1);

    return {'title': title, 'subtitle': subtitle};
};

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
        'locale': lang == 'pt' ? 'pt_BR' : 'en_US',
        'text': function(text, key) {
            switch (text) {
                case 'item_id':
                    return dictionary[DICT[dataset][text][squares]] || dictionary[text];
                case 'value':
                case 'kg':
                case 'value_per_kg':
                    return dictionary[DICT[dataset][text][args['type']]] || dictionary[text];
                case 'jobs':
                    return dictionary[DICT[dataset][text]];
                case 'primary connections':
                    return text.replace(/\w\S*/g, function(txt) {
                        return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();
                    })
                default:
                    return dictionary[text] || text;
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
                    if (symbol === 'k')
                        symbol = 'Mil';
                }

                result = value + ' ' + symbol;
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
                    result = '$' + result;
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
