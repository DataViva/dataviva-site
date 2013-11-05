import re, operator
from flask import Blueprint, request, render_template, flash, g, session, \
            redirect, url_for, jsonify, abort, make_response, Response
from dataviva import db
from dataviva.utils import make_query, crossdomain
from dataviva.secex.models import Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw

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

############################################################
# ----------------------------------------------------------
# 2 variable views
# 
############################################################

@mod.route('/all/<bra_id>/all/all/')
@mod.route('/<year>/<bra_id>/all/all/')
@crossdomain()
def secex_yb(**kwargs):
    return make_response(make_query(Yb_secex, request.args, **kwargs))

@mod.route('/all/all/<hs_id>/all/')
@mod.route('/<year>/all/<hs_id>/all/')
@crossdomain()
def secex_yp(**kwargs):
    return make_response(make_query(Yp, request.args, **kwargs))

@mod.route('/all/all/all/<wld_id>/')
@mod.route('/<year>/all/all/<wld_id>/')
@crossdomain()
def secex_yw(**kwargs):
    return make_response(make_query(Yw, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 3 variable views
# 
############################################################

@mod.route('/all/<bra_id>/all/<wld_id>/')
@mod.route('/<year>/<bra_id>/all/<wld_id>/')
@crossdomain()
def secex_ybw(**kwargs):
    return make_response(make_query(Ybw, request.args, **kwargs))

@mod.route('/all/<bra_id>/<hs_id>/all/')
@mod.route('/<year>/<bra_id>/<hs_id>/all/')
@crossdomain()
def secex_ybp(**kwargs):
    kwargs["join"] = [{
                        "table": Yp,
                        "columns": ["pci"],
                        "on": ["year", "hs_id"]
                    }]
    return make_response(make_query(Ybp, request.args, **kwargs))

@mod.route('/all/all/<hs_id>/<wld_id>/')
@mod.route('/<year>/all/<hs_id>/<wld_id>/')
@crossdomain()
def secex_ypw(**kwargs):
    return make_response(make_query(Ypw, request.args, **kwargs))

############################################################
# ----------------------------------------------------------
# 4 variable views
# 
############################################################

@mod.route('/all/<bra_id>/<hs_id>/<wld_id>/')
@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@crossdomain()
def secex_ybpw(**kwargs):
    return make_response(make_query(Ybpw, request.args, **kwargs))