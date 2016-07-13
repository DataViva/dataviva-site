from collections import namedtuple

DataSet = namedtuple('DataSet', ['id', 'dimensions', 'years'])
Dimension = namedtuple('Dimension', ['id', 'name', 'depths'])
Depth = namedtuple('Depth', ['id', 'value'])

locations = Dimension('bra', 'Location', [
    Depth('bra_1', 'regions'),
    Depth('bra_3', 'states'),
    Depth('bra_5', 'mesoregions'),
    Depth('bra_7', 'microregions'),
    Depth('bra_9', 'municipalities'),
])

industries = Dimension('cnae', 'Industry', [
    Depth('cnae_1', 'sections'),
    Depth('cnae_3', 'divisions'),
    Depth('cnae_6', 'classes'),
])

occupations = Dimension('cbo', 'Occupation', [
    Depth('cbo_1', 'main_groups'),
    Depth('cbo_4', 'families'),
])

products = Dimension('hs', 'Product', [
    Depth('hs_2', 'sections'),
    Depth('hs_6', 'position'),
])

trade_partners = Dimension('wld', 'TradePartner', [
    Depth('wld_2', 'continents'),
    Depth('wld_5', 'countries'),
])

courses = Dimension('course_sc', 'BasicCourse', [
    Depth('course_sc_2', 'field'),
    Depth('course_sc_5', 'course'),
])

majors = Dimension('course_hedu', 'Major', [
    Depth('course_hedu_2', 'field'),
    Depth('course_hedu_6', 'majors'),
])

universities = Dimension('university', 'University', [
    Depth('show', 'university'),
])

schools = Dimension('school', 'School', [
    Depth('show', 'school'),
])

attrs_datasets = [
    DataSet('rais', [locations, industries, occupations], [str(year) for year in range(2002, 2015)]),
    DataSet('secex', [locations, products, trade_partners], [str(year) for year in range(2002, 2017)]),
    DataSet('hedu', [locations, universities, majors], [str(year) for year in range(2009, 2015)]),
    DataSet('sc', [locations, schools, courses], [str(year) for year in range(2007, 2016)])
]
