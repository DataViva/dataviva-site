from flask import Blueprint, request, g, jsonify
from dataviva import db
import dataviva.api.hedu.models as hedu
from dataviva.utils.gzip_data import gzip_response
from sqlalchemy import func, distinct, desc
from dataviva.utils import make_query
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key
from dataviva.utils import table_helper, query_helper
from dataviva.utils.csv_helper import gen_csv, is_download

mod = Blueprint('hedu', __name__, url_prefix='/hedu')

@mod.route('/<year>/<bra_id>/<university_id>/<course_hedu_id>/')
@view_cache.cached(key_prefix=api_cache_key("hedu"), unless=is_download)
def hedu_api(**kwargs):
    tables = [hedu.Yb_hedu, hedu.Yc_hedu, hedu.Yu, hedu.Ybc_hedu, hedu.Ybu, hedu.Yuc, hedu.Ybuc]

    idonly = request.args.get('id', False) is not False
    limit = int(request.args.get('limit', 0) or kwargs.pop('limit', 0))
    order = request.args.get('order', None) or kwargs.pop('order', None)
    sort = request.args.get('sort', None) or kwargs.pop('sort', 'desc')
    offset = request.args.get('offset', None) or kwargs.pop('offset', None)
    if order and "." in order:
        order, sort = order.split(".")
    serialize = request.args.get('serialize', None) or kwargs.pop('serialize', True)
    exclude = request.args.get('exclude', None) or kwargs.pop('exclude', None)
    download = request.args.get('download', None) or kwargs.pop('download', None)

    if "university_id" in kwargs:
        # -- there is no nesting for university ids
        kwargs["university_id"] = kwargs["university_id"].replace("show.5", "show")

    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'university_id', 'course_hedu_id'], tables)
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, offset=offset, serialize=serialize)

    if serialize or download:
        response = jsonify(results)
        if download:
            return gen_csv(results, "hedu")
        return gzip_response(response)

    return results
