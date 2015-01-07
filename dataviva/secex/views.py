import re, operator
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, abort, make_response, Response
from dataviva import db
from dataviva.utils.make_query import make_query
from dataviva.secex.models import Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw
from dataviva.utils import table_helper

mod = Blueprint('secex', __name__, url_prefix='/secex')

@mod.errorhandler(404)
def page_not_found(error):
    return error, 404

@mod.after_request
def per_request_callbacks(response):
    if response.status_code != 302 and response.mimetype != "text/csv":
        response.headers['Content-Encoding'] = 'gzip'
        response.headers['Content-Length'] = str(len(response.data))
    return response

@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
def secex_api(**kwargs):
    # -- 1. filter ALLs
    kwargs = {k:v for k,v in kwargs.items() if v != table_helper.ALL}
    # -- 2. select table
    allowed_when_not, possible_tables = table_helper.prepare(["bra_id", "hs_id", "wld_id"], [Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw])
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)
    if table is Ybp:
        kwargs["join"] = [{"table": Yp, "columns": ["pci"], "on": ["year", "hs_id"]}]
    resp = make_query(table, kwargs, g.locale)
    return make_response(resp)
