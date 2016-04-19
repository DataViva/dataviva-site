from collections import namedtuple

DataSet = namedtuple('DataSet', ['id', 'dimensions', 'years'])
Dimension = namedtuple('Dimension', ['id', 'depths'])
Depth = namedtuple('Depth', ['id', 'value'])

locations = Dimension('bra', [
    Depth('bra_1', 'regions'),
    Depth('bra_3', 'states'),
    Depth('bra_5', 'mesoregions'),
    Depth('bra_7', 'microregions'),
    Depth('bra_9', 'municipalities'),
])

industries = Dimension('cnae', [
    Depth('cnae_1', 'sections'),
    Depth('cnae_3', 'divisions'),
    Depth('cnae_6', 'classes'),
])

occupations = Dimension('cbo', [
    Depth('cbo_1', 'main_groups'),
    Depth('cbo_4', 'families'),
])

products = Dimension('hs', [
    Depth('hs_2', 'sections'),
    Depth('hs_6', 'position')
])

trade_partners = Dimension('wld', [
    Depth('wld_2', 'continents'),
    Depth('wld_5', 'countries')
])

majors = Dimension('course_hedu', [
    Depth('course_hedu_2', 'field'),
    Depth('course_hedu_6', 'majors')
])

courses = Dimension('course_sc', [
    Depth('course_sc_2', 'field'),
    Depth('course_sc_5', 'course')
])

attrs_datasets = [
    DataSet('rais', [locations, industries, occupations], [str(year) for year in range(2002, 2014)]),
    DataSet('secex', [locations, products, trade_partners], [str(year) for year in range(2002, 2015)]),
    DataSet('hedu', [locations, majors], [str(year) for year in range(2009, 2014)]),
    DataSet('sc', [locations, courses], [str(year) for year in range(2007, 2015)])
]
