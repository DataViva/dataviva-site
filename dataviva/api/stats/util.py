# Utility functions for stats
import json

def parse_year(s):
    return int(str(s).split("-")[0])

def compute_allowed(table_dict):
    master_list = set([])
    for table in table_dict:
        master_list = master_list.union(table.__table__.columns.keys())

    for table in table_dict:
        table_dict[table] = master_list.difference(table.__table__.columns.keys())
    return table_dict


def gen_table_list(poss_tables):
    table_dict = {}
    for tname, tables in poss_tables.items():
        for table in tables:
            table_dict[table] = set()
    return table_dict

def get_profiles(item_list, typestr, serialize=True):
    from dataviva.api.attrs.models import Bra, Hs, Cbo, Cnae, Course_hedu, University

    typemap = {"bra": Bra, "hs": Hs, "cnae": Cnae, "cbo": Cbo, "course_hedu": Course_hedu, "university": University}
    obj = typemap[typestr]

    posters = [{"poster": obj.query.get(me).serialize(), "value": float(data)} for me,data in item_list]
    return posters

def get_year(table, mode):
    if mode == 'min':
        year_col = table.year.asc()
    else:
        year_col = table.year.desc()
    return table.query.with_entities(table.year).order_by(year_col).first().year

def get_month(table, year, mode):
    if mode == 'min':
        month_col = table.month.asc()
    else:
        month_col = table.month.desc()
    return table.query.with_entities(table.month).filter_by(year=year).filter(table.month!=0).order_by(month_col).first().month

def compute_table_years(datasets):
    from dataviva.api.secex.models import Ymb
    from dataviva.api.rais.models import Yb_rais
    from dataviva.api.hedu.models import Yc_hedu
    from dataviva.api.sc.models import Yc_sc
    from dataviva.api.attrs.models import Yb as Yb_attr
    from dataviva.api.attrs.models import Ybs

    tables = {"hedu": Yc_hedu, "sc": Yc_sc, "secex": Ymb, "rais": Yb_rais, "population": Yb_attr, "stats": Ybs}

    results = {}
    for dataset in datasets:
        max_year = str(get_year(tables[dataset], mode='max'))
        min_year = str(get_year(tables[dataset], mode='min'))
        if dataset == "secex":
            max_year = max_year + "-" + str(get_month(tables[dataset], max_year, 'max'))
            min_year = min_year + "-" + str(get_month(tables[dataset], min_year, 'min'))
        results[dataset] = [min_year, max_year]
    return results

def get_or_set_years(redis, key):
    val = redis.get(key)
    if val:
        val = json.loads(val)
    else:
        val = compute_table_years(['hedu', 'sc', 'secex', 'rais', 'population', 'stats'])
    redis.set(key, json.dumps(val))
    return val
