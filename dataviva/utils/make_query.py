import re, operator, sys
from itertools import groupby
from flask import abort, current_app, make_response, Flask, jsonify, request, Response, session
from decimal import Decimal
from sqlalchemy import func, and_, or_, asc, desc, not_

from dataviva.utils.cached_query import cached_query
from dataviva.utils.gzip_data import gzip_data

''' Given a "year" string from URL, turn this into an array of years
    as integers'''
def parse_years(year_str):
    year_str = str(year_str)
    if "-" in year_str:
        # we allow a range of years w/ or w/o interval (using '.' as sep)
        year_start, year_end = year_str.split("-")
        if "." in year_end:
            year_end, year_interval = year_end.split(".")
        else:
            year_interval = "1"
        years = range(int(year_start), int(year_end)+1, int(year_interval))
    else:
        # we allow a set of years (with '_' between)
        years = [int(y) for y in year_str.split("_")]
    return years

''' Returns array of ECIs given location '''
def location_values(ret,cat):

    from dataviva.api.secex.models import Ymb
    from dataviva.api.rais.models import Yb_rais

    bra_id = ret[cat][0]["id"]
    if bra_id != "all":
        ecis = Ymb.query.filter_by(bra_id=bra_id).all()
        ret["eci"] = {}
        for yb in ecis:
            ret["eci"][yb.year] = yb.eci
    return ret

''' Returns modified query and return variable for data calls '''
def parse_filter(kwargs,id_type,query,data_table,ret):

    from dataviva.api.attrs.models import Bra, Cnae, Cbo, Hs, Wld, University, Course_hedu, Course_sc

    query = query.group_by(getattr(data_table, id_type))
    cat = id_type[:-3]
    table = locals()[cat.capitalize()]
    ids = kwargs[id_type].split("_")
    id_list = []
    depth = None
    for id in ids:

        split_obj = id.split(".")

        kms = None
        if split_obj[0] != "all" and split_obj[0] != "show":
            obj_id = split_obj[0]
            if len(split_obj) > 1 and split_obj[1] != "show":
                kms = split_obj[1]
            ret_obj = table.query.get_or_404(obj_id).serialize()
        elif split_obj[0] == "all":
            obj_id = "all"
            if cat == "bra":
                ret_obj = Wld.query.get_or_404("sabra").serialize()
                ret_obj["id"] = "all"
            else:
                ret_obj = None
        else:
            obj_id = None
            ret_obj = None

        split_depth = id.split("show.")
        if len(split_depth) > 1:
            obj_depth = int(split_depth[1])
        else:
            obj_depth = None

        if obj_id:
            if kms:
                neighbors = table.query.get(obj_id).get_neighbors(kms)
                obj_list = []
                for m in neighbors:
                    if m.bra_id_dest == obj_id:
                        obj_list.append(m.bra_id_origin)
                    else:
                        obj_list.append(m.bra_id_dest)
                if "show" not in id:
                    ret_obj["aggregates"] = obj_list
                    ret["aggregate"] = True
                id_list = id_list + obj_list
            elif obj_depth and obj_depth > len(obj_id):
                # if "plr" in obj_id:
                #     obj_list = table.query.get(obj_id).pr.all()
                #     obj_list = [m.id for m in obj_list]
                #     id_list = id_list + obj_list
                # else:
                obj_list = table.query.filter(\
                    and_(func.char_length(getattr(table,"id")) == obj_depth, \
                    getattr(table,"id").startswith(obj_id)))
                munic_list = [d.id for d in obj_list.all()]
                id_list = id_list + munic_list
            elif obj_id == "all":
                if cat == "bra" or cat == "hs" or cat == "wld":
                    parent_depth = 2
                else:
                    parent_depth = 1
                obj_list = table.query.filter(func.char_length(getattr(table,"id")) == parent_depth)
                obj_list = [d.id for d in obj_list.all()]
                ret_obj["aggregates"] = obj_list
                ret["aggregate"] = True
                id_list = id_list + obj_list
            else:
                id_list.append(obj_id)
        elif obj_depth:
            depth = obj_depth

        if ret_obj:
            if cat not in ret:
                ret[cat] = []
            ret[cat].append(ret_obj)

    if len(id_list) > 0:
        query = query.filter(getattr(data_table,id_type).in_(id_list))
    elif depth:
        query = query.filter(func.char_length(getattr(data_table,id_type)) == depth)

    if cat == "bra" and obj_id:
        if len(ret[cat]) == 0:
            ret[cat].append(Wld.query.get_or_404("sabra").serialize())
        ret = location_values(ret,cat)

    return {"query": query, "ret": ret}


def merge_objects(objs):

    averages = ['eci', 'eci_wld', 'pci', 'unique_cnae', 'unique_cbo',
                'unique_hs', 'unique_wld', 'importance',
                'val_usd_growth_pct', 'val_usd_growth_pct_5',
                'export_val_growth_pct', 'export_val_growth_pct_5',
                'import_val_growth_pct', 'import_val_growth_pct_5',
                'wage_growth_pct', 'wage_growth_pct_5',
                'num_emp_growth_pct', 'num_emp_growth_pct_5',
                'distance', 'distance_wld',
                'opp_gain', 'opp_gain_wld',
                'rca', 'rca_wld']

    ret_obj = {}
    for obj in objs:
        for k in obj:
            values = []
            if k == "wage_avg":
                num_jobs = []
            elif k == "num_jobs_est":
                num_est = []
            for obj2 in objs:
                if k in obj2:
                    if isinstance(obj2[k],str) or isinstance(obj2[k],unicode):
                        values = obj2[k]
                    elif isinstance(obj2[k],Decimal) or isinstance(obj2[k],long) \
                      or isinstance(obj2[k],float) or isinstance(obj2[k],int):
                        if k == "num_jobs_est":
                            num_est.append(float(obj2["num_est"]))
                            values.append(float(obj2["num_jobs"]))
                        elif k == "wage_avg":
                            num_jobs.append(float(obj2["num_jobs"]))
                            values.append(float(obj2["wage"]))
                        else:
                            values.append(float(obj2[k]))
            if len(values) > 0:
                if not isinstance(values,str) and not isinstance(values,unicode):
                    if k == "num_jobs_est":
                        ret_obj[k] = sum(values)/sum(num_est)
                    elif k == "wage_avg":
                        ret_obj[k] = sum(values)/sum(num_jobs)
                    elif k in averages:
                        ret_obj[k] = sum(values)/len(values)
                    else:
                        ret_obj[k] = sum(values)
                else:
                    ret_obj[k] = values
            else:
                ret_obj[k] = None
    return ret_obj

def compile_query(query):
    from sqlalchemy.sql import compiler
    from MySQLdb.converters import conversions, escape

    dialect = query.session.bind.dialect
    statement = query.statement
    comp = compiler.SQLCompiler(dialect, statement)
    comp.compile()
    enc = dialect.encoding
    params = []
    for k in comp.positiontup:
        v = comp.params[k]
        if isinstance(v, unicode):
            v = v.encode(enc)
        params.append( escape(v, conversions) )
    return (comp.string.encode(enc) % tuple(params)).decode(enc)



def make_query(data_table, url_args, lang, **kwargs):

    from dataviva import db
    from dataviva.api.attrs.models import Bra, Cnae, Cbo, Hs, Wld, University, Course_hedu, Course_sc

    ops = {">": operator.gt,
           ">=": operator.ge,
           "<": operator.lt,
           "<=": operator.le}

    check_keys = ["bra_id", "cnae_id", "cbo_id", "hs_id", "wld_id", "university_id", "course_hedu_id", "course_sc_id"]
    unique_keys = []

    download = url_args.get("download", None)
    raw = True if "raw" in kwargs else None
    order = url_args.get("order", None)
    offset = url_args.get("offset", None)
    limit = url_args.get("limit", None)
    cols = url_args.get("cols", None)
    if type(cols) == str or type(cols) == unicode:
        cols = cols.split(".")
    excluding = url_args.get("excluding", None)
    if offset:
        offset = float(offset)
        limit = limit or 50
    filter = url_args.get("filter", None)
    if filter:
        filter = re.split("(>=|>|<=|<)", filter)
    join = kwargs["join"] if "join" in kwargs else False
    show_id = None
    cache_id = request.path
    ret = {}
    # first lets test if this query is cached (be sure we are not paginating
    # results) as these should not get cached
    if limit is None and download is None and raw is None and cols is None:
        cached_q = cached_query(cache_id)
        if cached_q:
            return cached_q

    query = db.session.query(data_table)
    if join:
        for j in join:
            query = query.add_entity(j["table"])
            for col in j["on"]:
                query = query.filter(getattr(data_table, col) == getattr(j["table"], col))

    query = query.group_by(data_table.year)

    # handle year (if specified)
    if "year" in kwargs:
        ret["year"] = parse_years(kwargs["year"])
        query = query \
            .filter(data_table.year.in_(ret["year"]))

    # parse all filters
    for key in check_keys:
        if key in kwargs:
            if key != "bra_id":
                unique_keys.append(key)
            if "show" in kwargs[key]:
                show_id = key
            parse_results = parse_filter(kwargs,key,query,data_table,ret)
            query = parse_results["query"]
            ret = parse_results["ret"]

    if filter:
        query = query.filter(ops[filter[1]](getattr(data_table, filter[0]), float(filter[2])))

    if excluding:
        for e in excluding:
            query = query.filter(not_(getattr(data_table, e).startswith(excluding[e])))

    # lastly we want to get the actual data held in the table requested
    if "aggregate" not in ret:
        # handle ordering
        if order:
            direction = "asc"

            if "." in order:
                o, direction = order.split(".")
            else:
                o = order

            order_table = None
            if join:
                for j in join:
                    if o in j["columns"]:
                        order_table = j["table"]

            if order_table == None:
                order_table = data_table

            all_col_names = data_table.__table__.columns.keys() + order_table.__table__.columns.keys()
            if o in all_col_names:
                if direction == "asc":
                    query = query.order_by(asc(getattr(order_table,o)))
                elif direction == "desc":
                    query = query.order_by(desc(getattr(order_table,o)))

        if limit:
            query = query.limit(limit).offset(offset)

    # raise Exception(compile_query(query))
    if join:
        ret["data"] = []
        items = query.all()
        for row in items:
            datum = row[0].serialize()
            join_data = []
            for i, r in enumerate(row):
                if i != 0:
                    serialized = r.serialize()
                    for k in serialized:
                        if k in join[i-1]["columns"]:
                            datum[k] = serialized[k]
            ret["data"].append(datum)
    elif raw:
        return query.all()
    else:
        ret["data"] = [d.serialize() for d in query.all()]

    if "aggregate" in ret:

        agg_data = []
        ret["data"] = sorted(ret["data"],key=lambda x: x["year"])

        if "bra" not in ret:
            ret["bra"] = {}

        for bra in ret["bra"]:

            if "aggregates" in bra:
                filtered_objs = []
                for key, group in groupby(ret["data"],lambda x: x["year"]):
                    year_data = []
                    for obj in group:
                        if obj["bra_id"] in bra["aggregates"]:
                            year_data.append(obj)

                    if len(unique_keys) > 0:

                        def check_filter(d,keys,i):
                            if i == len(keys):
                                merged_data = merge_objects(d)
                                merged_data["year"] = key
                                merged_data["bra_id"] = bra["id"]
                                agg_data.append(merged_data)
                            else:
                                d = sorted(d,key=lambda x: x[keys[i]])
                                for x, g in groupby(d,lambda x: x[keys[i]]):
                                    new_array = []
                                    for o in g:
                                        new_array.append(o)
                                    check_filter(new_array,keys,i+1)

                        check_filter(year_data,unique_keys,0)
                    else:
                        merged_data = merge_objects(year_data)
                        merged_data["year"] = key
                        merged_data["bra_id"] = bra["id"]
                        agg_data.append(merged_data)
            else:
                bra_data = [obj for obj in ret["data"] if obj["bra_id"] == bra["id"]]
                agg_data = agg_data + bra_data
        ret["data"] = agg_data

        # handle ordering
        if order:
            direction = "asc"
            if "." in order:
                o, direction = order.split(".")
            else:
                o = order
            if direction == "asc":
                ret["data"].sort(key=lambda x: x[o] if o in x else None)
            elif direction == "desc":
                ret["data"].sort(key=lambda x: x[o] if o in x else None, reverse=True)

        if limit:
            ret["data"] = ret["data"][int(offset):int(offset)+int(limit)]

    if cols:
        cols = ["year","bra_id"]+unique_keys+cols
        new_return = []
        attrs = None
        if ("name" or "id_ibge" or "id_mdic" in cols) and show_id:
            attr_table = locals()[show_id[:-3].capitalize()]
            attrs = [x.serialize() for x in attr_table.query.all()]
            attrs = {x["id"]:x or None for x in attrs}
        for d in ret["data"]:
            new_obj = {}
            for k in d:
                if k in cols:
                    new_obj[k] = d[k]
            if attrs:
                if "name" in cols and "name_{0}".format(lang) in attrs[d[show_id]]:
                    new_obj["name"] = attrs[d[show_id]]["name_{0}".format(lang)]
                if "id_ibge" in cols and "id_ibge" in attrs[d[show_id]]:
                    new_obj["id_ibge"] = attrs[d[show_id]]["id_ibge"]
                if "id_mdic" in cols and "id_mdic" in attrs[d[show_id]]:
                    new_obj["id_mdic"] = attrs[d[show_id]]["id_mdic"]
            new_return.append(new_obj)
        ret["data"] = new_return

    if order:
        for i, d in enumerate(ret["data"]):
            r = i+1
            if offset:
                r = r+offset
            d["rank"] = int(r)

    if download is not None:
        header = [str(c).split(".")[1] for c in data_table.__table__.columns]
        if cols:
            stickies = [c for c in header if c in unique_keys]
            header = stickies+cols

        def generate():
            for i, data_dict in enumerate(ret["data"]):
                row = [str(data_dict[c]) if c in data_dict else '' for c in header]
                if i == 0:
                    yield ';'.join(header) + '\n' + ';'.join(row) + '\n'
                yield ';'.join(row) + '\n'

        content_disposition = "attachment;filename=%s.csv" % (cache_id[1:-1].replace('/', "_"))

        if sys.getsizeof(ret["data"]) > 10485760:
            resp = Response(['Unable to download, request is larger than 10mb'],
                            mimetype="text/csv;charset=UTF-8",
                            headers={"Content-Disposition": content_disposition})
        else:
            resp = Response(generate(), mimetype="text/csv;charset=UTF-8",
                            headers={"Content-Disposition": content_disposition})
        return resp

    # gzip and jsonify result
    ret = gzip_data(jsonify(ret).data)

    if limit is None and download is None and raw is None and cols is None:
        cached_query(cache_id, ret)

    return ret
