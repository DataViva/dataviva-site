from flask import Blueprint, request, jsonify
from dataviva import db
from dataviva.api.sc.models import Yb_sc, Yc_sc, Ys, Ybs, Ybc_sc, Ybsc, Ysc
from dataviva.api.attrs.models import School
from dataviva.utils.gzip_data import gzip_response
from dataviva.utils import make_query
from dataviva import view_cache
from dataviva.utils.cached_query import api_cache_key
from dataviva.utils import table_helper, query_helper
from dataviva.utils.csv_helper import gen_csv, is_download

mod = Blueprint('sc', __name__, url_prefix='/sc')

@mod.route('/<year>/<bra_id>/<school_id>/<course_sc_id>/')
@view_cache.cached(key_prefix=api_cache_key("sc"), unless=is_download)
def sc_api(**kwargs):
    tables = [Yc_sc, Yb_sc, Ys, Ybc_sc, Ybs, Ysc, Ybsc]

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

    only_vocational = False
    if "school_id" in kwargs:
        # -- there is no nesting for school ids
        kwargs["school_id"] = kwargs["school_id"].replace("show.8", "show")
        only_vocational = "show" in kwargs["school_id"] and not "xx" in kwargs["course_sc_id"] and exclude == "xx%"
        if only_vocational:
            exclude = None

    # -- 2. select table
    allowed_when_not, possible_tables = table_helper.prepare(['bra_id', 'school_id', 'course_sc_id'], tables)
    table = table_helper.select_best_table(kwargs, allowed_when_not, possible_tables)

    if not table:
        raise Exception("No table!")

    filters, groups, show_column = query_helper.build_filters_and_groups(table, kwargs, exclude=exclude)

    if only_vocational:
        vschools = School.query.with_entities(School.id).filter(School.is_vocational == 1).all()
        vschools = [v.id for v in vschools]
        filters.append(table.school_id.in_(vschools))

    results = query_helper.query_table(table, filters=filters, groups=groups, limit=limit, order=order, sort=sort, offset=offset, serialize=serialize)

    if serialize or download:
        response = jsonify(results)
        if download:
            return gen_csv(results, "sc")
        return gzip_response(response)

    return results
