from collections import namedtuple

DataBase = namedtuple('DataBase', ['dimensions', 'years'])
Dimension = namedtuple('Dimension', ['id', 'depths'])
Depth = namedtuple('Depth', ['id', 'value'])

locations = Dimension('bra_plural', [
    Depth('bra_1', 'regions'),
    Depth('bra_3', 'states'),
    Depth('bra_5', 'mesoregions'),
    Depth('bra_7', 'microregions'),
    Depth('bra_9', 'municipalities'),
])

industries = Dimension('cnae_plural', [
    Depth('cnae_1', 'sections'),
    Depth('cnae_3', 'divisions'),
    Depth('cnae_6', 'classes'),
])

occupations = Dimension('cbo_plural', [
    Depth('cbo_1', 'main_groups'),
    Depth('cbo_4', 'families'),
])

products = Dimension('hs_plural', [
    Depth('hs_2', 'sections'),
    Depth('hs_6', 'position')
])

trade_partners = Dimension('wld_plural', [
    Depth('wld_2', 'continents'),
    Depth('wld_5', 'countries')
])

majors = Dimension('course_hedu_plural', [
    Depth('course_hedu_2', 'field'),
    Depth('course_hedu_6', 'majors')
])

courses = Dimension('course_sc_plural', [
    Depth('course_sc_2', 'field'),
    Depth('course_sc_5', 'course')
])

attrs_databases = {
    'rais': DataBase([locations, industries, occupations], [str(year) for year in range(2002, 2014)]),
    'secex': DataBase([locations, products, trade_partners], [str(year) for year in range(2002, 2015)]),
    'hedu': DataBase([locations, majors], [str(year) for year in range(2009, 2014)]),
    'sc': DataBase([locations, courses], [str(year) for year in range(2007, 2015)])
}
