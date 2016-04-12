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


attrs_databases = {
    'rais': DataBase([locations, occupations, industries], [str(year) for year in range(2002, 2014)]),
}
