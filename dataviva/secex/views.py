from flask import Blueprint, request, jsonify
from dataviva import db
# from dataviva.utils.make_query import make_query
from dataviva.secex.models import Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw
from dataviva.utils import table_helper, query_helper
from dataviva.utils.gzip_data import gzipped
from dataviva.utils.decorators import cache_api

mod = Blueprint('secex', __name__, url_prefix='/secex')

@mod.route('/<year>/<bra_id>/<hs_id>/<wld_id>/')
@gzipped
@cache_api("secex")
def secex_api(**kwargs):
    limit = int(kwargs.pop('limit', 0)) or int(request.args.get('limit', 0) )
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    zeros = request.args.get('zeros', False) or kwargs.pop('zeros', False)
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)

    # -- 1. filter ALLs
    kwargs = {k:v for k,v in kwargs.items() if v != table_helper.ALL}
    # -- 2. select table
    allowed_when_not, possible_tables = table_helper.prepare(["bra_id", "hs_id", "wld_id"], [Yb_secex, Yw, Yp, Ybw, Ybp, Ypw, Ybpw])
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)
    if serialize:
        return jsonify(results)

    return results
