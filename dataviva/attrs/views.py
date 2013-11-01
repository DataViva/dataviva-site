from sqlalchemy import func, distinct
from flask import Blueprint, request, jsonify, abort, g

from dataviva import db, __latest_year__
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
    lang = request.args.get('lang', None) or g.locale
    # if response.status_code != 302:
    if response.status_code != 302 and request.is_xhr:
        cache_id = request.path + lang
        # test if this query was cached, if not add it
        cached_q = cached_query(cache_id)
        if cached_q is None:
            response.data = gzip_data(response.data)
            cached_query(cache_id, response.data)
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

def fix_name(attr, lang):
    name_lang = "name_" + lang
    desc_lang = "desc_" + lang
    keywords_lang = "keywords_" + lang
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

def get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, 
                        Attr_weight_mergeid, Attr_id_lens, lang):
    # this is the dictionary that will be jsonified and sent to the user
    ret = {}
    dataset = "rais"
    if Attr == Cbo or Attr == Hs:
        dataset = "secex"
    latest_year = __latest_year__[dataset]
        
    cache_id = request.path + lang
    # first lets test if this query is cached
    cached_q = cached_query(cache_id)
    if cached_q and request.is_xhr:
        return cached_q
    
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
        
        ret["data"] = [fix_name(a.serialize(), lang) for a in attrs]
    # an ID/filter was not provided
    else:
        
        attrs_all = Attr.query.filter(func.char_length(Attr.id) <= Attr_id_lens[-1]).all()
        
        # just get items available in DB
        attrs_val = Attr_weight_tbl.query.filter(Attr_weight_tbl.year == latest_year).all()
        attrs_val = {getattr(a, Attr_weight_mergeid): getattr(a, Attr_weight_col) for a in attrs_val}
        
        attrs_w_data = db.session.query(Attr, func.sum(getattr(Attr_weight_tbl, Attr_weight_col)))
        attrs_w_data = attrs_w_data \
                        .filter(getattr(Attr_weight_tbl, Attr_weight_mergeid) == Attr.id).group_by(Attr)
        attrs_w_data = {a[0].id: a[1] for a in attrs_w_data}
                        
        attrs = []
        for a in attrs_all:
            a = a.serialize()
            a["available"] = False
            a[Attr_weight_col] = 0
            if a["id"] in attrs_w_data:
                a["available"] = True
                if a["id"] in attrs_val:
                    a[Attr_weight_col] = attrs_val[a["id"]]
            if Attr_weight_col == "population":
                if len(a["id"]) == 8 and a["id"][:2] == "mg":
                    plr = Bra.query.get_or_404(a["id"]).pr2.first()
                    if plr: a["plr"] = plr.id
            attrs.append(fix_name(a, lang))
        
        ret["data"] = attrs
        
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
    lang = request.args.get('lang', None) or g.locale
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens, lang)
    
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
    lang = request.args.get('lang', None) or g.locale
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens, lang)

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
    lang = request.args.get('lang', None) or g.locale
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens, lang)

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
    lang = request.args.get('lang', None) or g.locale
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens, lang)

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
    lang = request.args.get('lang', None) or g.locale
    
    return get_attrs(Attr, Attr_id, Attr_weight_tbl, Attr_weight_col, Attr_weight_mergeid, Attr_id_lens, lang)