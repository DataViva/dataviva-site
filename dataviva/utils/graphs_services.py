def location_service(id_ibge):
    locations = {1: 'region', 2: 'state', 4: 'mesoregion',
                 5: 'microregion', 7: 'municipality'}
    return (locations[len(id_ibge)], id_ibge)


def wld_service(wld):
    if wld.isdigit():
        wld = '%03d' % int(wld)
    wlds = {2: 'continent', 3: 'country'}
    return (wlds[len(wld)], wld)


def product_service(product):
    if len(product) == 2:
        return ('product_section', product[:2])
    if len(product) == 4:
        return ('product_chapter', product[2:4])
    return ('product', product[2:])


def occupation_service(occupation):
    occupations = {1: 'occupation_group', 4: 'occupation_family'}
    return (occupations[len(occupation)], occupation)


def industry_service(industry):
    if len(industry) == 1:
        return ('industry_section', industry)
    if len(industry) == 3:
        return ('industry_division', industry[1:])
    return ('industry_class', industry[1:])


def filter_service(key):
    if key in ['region', 'state', 'mesoregion', 'microregion', 'municipality']:
        return 'location'
    if key in ['continent', 'country']:
        return 'partner'
    if key in ['industry_division', 'industry_section', 'industry_class']:
        return 'industry'
    if key in ['occupation_group', 'occupation_family']:
        return 'occupation'
    if key in ['product_section', 'product_chapter', 'product']:
        return 'product'
    if key in ['equipment_type', 'equipment_code']:
        return 'equipment'
    if key in ['bed_type', 'bed_type_per_specialty']:
        return 'bed_type'
    return key
