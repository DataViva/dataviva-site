from flask import Blueprint, request, jsonify
from dataviva import db
from dataviva.ei.models import Ymr, Yms, Ymsr
from dataviva.utils.gzip_data import gzipped
from dataviva.utils import make_query
from dataviva.utils.decorators import cache_api
from dataviva.utils import table_helper, query_helper

mod = Blueprint('ei', __name__, url_prefix='/ei')

@mod.route('/<year>-<month>/<bra_id_s>/<bra_id_r>/')
@mod.route('/<year>/<bra_id_s>/<bra_id_r>/')
@gzipped
# @cache_api("ei")
def ei_api(**kwargs):
    tables = [Ymr, Yms, Ymsr]
    
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    if order and "." in order:
        order, sort = order.split(".") 
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)

    if not "month" in kwargs:
        kwargs["month"] = query_helper.ALL

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id_r', 'bra_id_s', 'month', 'year'], tables)
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    if not table:
        raise Exception("No table!")

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if serialize or download:
        response = jsonify(results)
        if download:
            response.headers["Content-Disposition"] = "attachment;filename=ei_data.json"
        return response

    return results
