from sqlalchemy import func, distinct
from flask import Blueprint, request, jsonify, abort, g

from dataviva import db
from dataviva.attrs.models import Bra, Wld, Hs, Isic, Cbo, Yb
from dataviva.secex.models import Yp, Yw
from dataviva.rais.models import Yi, Yo
from dataviva.utils import exist_or_404, gzip_data, cached_query, title_case, crossdomain

mod = Blueprint('attrs', __name__, url_prefix='/attrs')

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

@mod.after_request
def after_request(response):
    # if response.status_code != 302:
    if response.status_code != 302 and request.is_xhr:
        cache_id = request.path + g.locale
        # test if this query was cached, if not add it
        cached_q = cached_query(cache_id)
        if cached_q is None:
            response.data = gzip_data(response.data)
            cached_query(cache_id, response.data)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

def fix_name(attr):
    name_lang = "name_" + g.locale
    desc_lang = "desc_" + g.locale
    keywords_lang = "keywords_" + g.locale
    if desc_lang in attr:
        attr["desc"] = title_case(attr[desc_lang])
        if "desc_en" in attr: del attr["desc_en"]
        if "desc_pt" in attr: del attr["desc_pt"]
    if name_lang in attr:
        attr["name"] = title_case(attr[name_lang])
        if "name_en" in attr: del attr["name_en"]
        if "name_pt" in attr: del attr["name_pt"]
    if keywords_lang in attr:
        attr["keywords"] = title_case(attr[keywords_lang])
        if "keywords_en" in attr: del attr["keywords_en"]
        if "keywords_pt" in attr: del attr["keywords_pt"]
    return attr

############################################################
# ----------------------------------------------------------
# All attribute views
# 
############################################################

def get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens):
    
    # this is the dictionary that will be jsonified and sent to the user
    ret = {}
    
    # if an ID is supplied only return that
    if Attr_id:
        
        # the '.show.' indicates that we are looking for a specific nesting
        if ".show." in Attr_id:
            this_attr, ret["nesting_level"] = Attr_id.split(".show.")
            # filter table by requested nesting level
            attrs = Attr.query \
                    .filter(Attr.id.startswith(this_attr)) \
                    .filter(func.char_length(Attr.id) == ret["nesting_level"]).all()

        # the 'show.' indicates that we are looking for a specific nesting
        elif "show." in Attr_id:
            ret["nesting_level"] = Attr_id.split(".")[1]
            # filter table by requested nesting level
            attrs = Attr.query.filter(func.char_length(Attr.id) == ret["nesting_level"]).all()
        
        # the '.' here means we want to see all attrs within a certain distance
        elif "." in Attr_id:
            this_attr, distance = Attr_id.split(".")
            this_attr = Attr.query.get_or_404(this_attr)
            attrs = this_attr.get_neighbors(distance)
        
        else:
            attrs = [Attr.query.get_or_404(Attr_id)]
        
        ret["data"] = [fix_name(a.serialize()) for a in attrs]
    # an ID/filter was not provided
    else:
        
        cache_id = request.path + g.locale
        # first lets test if this query is cached
        cached_q = cached_query(cache_id)
        if cached_q and request.is_xhr:
            return cached_q
        
        # this will be the lookup we'll use for getting parents
        # attrs = Attr.query.all()
        attrs = {a.id: fix_name(a.serialize()) for a in Attr.query.filter(func.char_length(Attr.id) <= Attr_id_lens[-1]).all()}
        
        # merge cbo table to YO table to find all instances in the data
        max_year = db.session.query(Attr_weight_tbl.year.distinct()).order_by(Attr_weight_tbl.year.desc()).all()[0]
        
        attrs_in_db = db.session.query(Attr, func.sum(getattr(Attr_weight_tbl, Attr_weight_col)))
        attrs_in_db = attrs_in_db \
                        .filter(getattr(Attr_weight_tbl, Attr_weight_mergeid) == Attr.id).group_by(Attr) \
                        .filter(Attr_weight_tbl.year == max_year[0])
        # attrs_in_db = {a[0].id: a for a in attrs_in_db.all()}
        
        if Attr_weight_col == "population":
            for a in attrs:
                if len(a) == 8 and a[:2] == "mg":
                    plr = Bra.query.get_or_404(a).pr2.first()
                    if plr:
                        attrs[a]["plr"] = plr.id
                        
        # raise Exception(attrs_in_db)
        
        for a in attrs_in_db.all():
            # this_id = a[0].id
            # attrs[this_id][Attr_weight_col] = a[1]
            attrs[a[0].id][Attr_weight_col] = int(a[1])
            attrs[a[0].id]["available"] = True
            # raise Exception(this_id[:id_len])
        # raise Exception(attrs["14"])
        
        
        # raise Exception(len(attrs.keys()))
        
        # raise Exception(len(attrs_in_db.keys()))
        
        # use a set so we don't have to worry about duplicates
        # for i, a in enumerate(attrs):
        #     if a.id in attrs_in_db:
        #         attrs[i] = attrs_in_db[a.id]
                # raise Exception(attrs_in_db[a.id])
            # attrs.add(a)
            # for id_len in Attr_id_lens[:-1]:
            #     attrs.add(attr_lookup.get(a[0].id[:id_len], a))
        
        # raise Exception(len(attrs))
        
        ret["data"] = attrs.values()
        
        # for a in attrs:
        #     if type(a) == Attr:
        #         ret["data"].append(fix_name(a.serialize()))
        #     else:
        #         ret["data"].append(dict(fix_name(a[0].serialize()), **{"available":True, Attr_weight_col: int(a[1])}))
    return jsonify(ret)

@mod.route('/bra/')
@mod.route('/bra/<bra_id>/')
@crossdomain()
def attrs_bra(bra_id=None):
    Attr = Bra
    Attr_id = bra_id
    Attr_weight_tbl = Yb
    Attr_weight_col = "population"
    Attr_weight_mergeid = "bra_id"
    Attr_id_lens = [2, 4, 6, 8]
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens)
    
@mod.route('/wld/')
@mod.route('/wld/<wld_id>/')
@crossdomain()
def attrs_wld(wld_id=None):
    Attr = Wld
    Attr_id = wld_id
    Attr_weight_tbl = Yw
    Attr_weight_col = "val_usd"
    Attr_weight_mergeid = "wld_id"
    Attr_id_lens = [2, 5]
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens)

@mod.route('/hs/')
@mod.route('/hs/<hs_id>/')
@crossdomain()
def attrs_hs(hs_id=None):
    Attr = Hs
    Attr_id = hs_id
    Attr_weight_tbl = Yp
    Attr_weight_col = "val_usd"
    Attr_weight_mergeid = "hs_id"
    Attr_id_lens = [2, 4, 6]
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens)

@mod.route('/isic/')
@mod.route('/isic/<isic_id>/')
@crossdomain()
def attrs_isic(isic_id=None):
    Attr = Isic
    Attr_id = isic_id
    Attr_weight_tbl = Yi
    Attr_weight_col = "num_emp"
    Attr_weight_mergeid = "isic_id"
    Attr_id_lens = [1, 3, 5]
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens)

@mod.route('/cbo/')
@mod.route('/cbo/<cbo_id>/')
@crossdomain()
def attrs_cbo(cbo_id=None):
    Attr = Cbo
    Attr_id = cbo_id
    Attr_weight_tbl = Yo
    Attr_weight_col = "num_emp"
    Attr_weight_mergeid = "cbo_id"
    Attr_id_lens = [1, 2, 3, 4]
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens)