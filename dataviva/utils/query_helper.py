import re
from dataviva import db
from sqlalchemy import func, desc, or_
from dataviva.api.attrs.models import bra_pr, Bra
from dataviva.translations.dictionary import dictionary

SHOW='show'
SHOW2='.show.'
ALL='all'
LEN='_len'
OR='_'

def bra_profiles(bra_ids):
    if not bra_ids:
        return []
    return Bra.query.filter(Bra.id.in_(bra_ids)).all()

def parse_value(column, value):
    if OR in str(value):
        return column.in_(value.split(OR))
    return column == value

def query_table(table, columns=[], filters=[], groups=[], limit=0, order=None, sort="desc", offset=None, serialize=True, having=[]):
    non_len_cols = [c for c in table.__table__.columns if not c.key.endswith("_len")]
    columns = columns or non_len_cols
    headers = [c.key for c in columns]
    if isinstance(order, (str, unicode)) and hasattr(table, order):
        filters.append(getattr(table, order) != None)
    # raise Exception(having)
    query = table.query \
        .with_entities(*columns) \
        .filter(*filters) \
        .group_by(*groups)
    if having:
        query = query.having(*having)
    if order:
        if sort != "asc":
            order = desc(order)
        query = query.order_by(order)
    if limit:
        query = query.limit(limit)
    if offset:
        query = query.offset(offset)
    # raise Exception(query)
    if serialize:
        data = {
            "headers": headers,
            "data": [ list(row) for row in query]
        }
    else:
        column_names = [c.key for c in columns]
        data = [dict(zip(column_names, vals)) for vals in query.all()]
    
    if  'bra_id' in data['headers']:
        index_bra = data['headers'].index('bra_id')
        data['headers'].insert(0, dictionary()['bra'])
        
        location_name = {}
        for location in Bra.query.all():
            location_name[location.id] = location.name()

        for i, row  in enumerate(data['data']):
            data['data'][i].insert(0, location_name[row[index_bra]])  
                              
    return data

def _show_filters_to_add(column, value, table, colname):
    to_add = []
    pattern = '(\w+)?\.?show\.?(\w+)?'
    matches = re.match(pattern, value)
    if matches:
        prefix, length = matches.groups()
        # PLANNING_REGION = "4mgplr"
        # if prefix and prefix.startswith(PLANNING_REGION) and length == '9':
        #     result = db.session.query(bra_pr).filter_by(pr_id=prefix).all()
        #     result = [muni for muni, pr in result]
        #     to_add.append(column.in_(result))
        if prefix:
            if OR in prefix:
                prefixes = prefix.split(OR)
                prefix_conds = [column.startswith(p) for p in prefixes]
                to_add.append(or_(*prefix_conds))
            else:
                to_add.append(column.startswith(prefix))

        if length and hasattr(table, colname + LEN):
            lencol = getattr(table, colname + LEN)
            to_add.append(lencol == length)
        # else, the assumption is that IFF a column doesn't have a length col associated with it
        # then it isn't nested and therefore an additional filter is not needed.
    return to_add

def build_filters_and_groups(table, kwargs, exclude=None):
    filters = []
    groups = []
    show_column = None

    for colname in kwargs:
        value = str(kwargs[colname])
        if colname == "month" and value == ALL:
            column = getattr(table, colname)
            filters.append(column.in_([1,2,3,4,5,6,7,8,9,10,11,12]))
            groups.append(column)
        elif value != ALL:
            # -- if the value is not "ALL", then we need to group by this column
            column = getattr(table, colname)
            groups.append(column)

            if not SHOW in value: # -- if the value does not include a SHOW operation, then just filter based on value
                filters.append(parse_value(column, value))
            else:
                show_column = column # -- set this as the show column
                filters += _show_filters_to_add(column, value, table, colname)

        elif colname in ["year", "month"]:
            column = getattr(table, colname)
            groups.append(column)

    if len(table.__name__) == len(groups):
        groups = []

    if exclude:
        if type(exclude) in [str, unicode]:
            if "%" in exclude:
                filters.append(~show_column.like(exclude))
            else:
                filters.append(show_column != exclude)
        else:
            filters.append(~show_column.in_(exclude))
    return filters, groups, show_column

def convert_filters(table, kwargs, remove=None):
    fake_kwargs = {k:v for k,v in kwargs.items() if not k in remove}
    return build_filters_and_groups(table, fake_kwargs)
