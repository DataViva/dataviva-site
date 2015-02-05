from flask import Blueprint, request, jsonify
from dataviva import db
from dataviva.sc.models import Yb_sc, Yc_sc, Ys, Ybs, Ybc_sc, Ybsc, Ysc
from dataviva.utils.gzip_data import gzipped
from dataviva.utils import make_query
from dataviva.utils.decorators import cache_api
from dataviva.utils import table_helper, query_helper

mod = Blueprint('sc', __name__, url_prefix='/sc')

@mod.route('/<year>/<bra_id>/<school_id>/<course_sc_id>/')
@gzipped
# @cache_api("sc")
def sc_api(**kwargs):
    tables = [Yc_sc, Yb_sc, Ys, Ybc_sc, Ybs, Ysc, Ybsc]

    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    if order and "." in order:
        order, sort = order.split(".")
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)

    if "school_id" in kwargs:
        # -- there is no nesting for university ids
        kwargs["school_id"] = kwargs["school_id"].replace("show.5", "show")

    # -- 2. select table
    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'school_id', 'course_sc_id'], tables)
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    if not table:
        raise Exception("No table!")

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, serialize=serialize)

    if serialize or download:
        response = jsonify(results)
        if download:
            response.headers["Content-Disposition"] = "attachment;filename=hedu_data.json"
        return response

    return results
