# Utility functions for stats
import json
from dataviva.attrs.models import Bra, Hs, Cbo, Cnae


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
    typemap = {"bra": Bra, "hs": Hs, "cnae": Cnae, "cbo": Cbo}
    obj = typemap[typestr]

    posters = [obj.query.get(me)for me in item_list]
    if serialize:
        posters = [p.serialize() for p in posters]
    return posters