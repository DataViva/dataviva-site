# views.py
from dataviva import db, lm
from dataviva.utils.exist_or_404 import exist_or_404
from flask import Blueprint, request, render_template, flash, g, session, redirect, url_for, jsonify, abort, current_app
from dataviva.api.stats.helper import compute_stats, stats_list, top_occupations
from dataviva.api.stats.helper import CAROUSEL_NS
from dataviva.api.stats.util import get_profiles
from dataviva import view_cache
from dataviva.utils.cached_query import make_cache_key
from flask.ext.babel import get_locale
from dataviva.utils.gzip_data import gzipped

from dataviva.api.stats.cache import profile_cache_serialized

import json

mod = Blueprint('stats', __name__, url_prefix='/stats')

def make_cache_key(*args, **kwargs):
    path = request.path
    args = str(hash(frozenset(request.args.items())))
    lang = str(get_locale())
    return CAROUSEL_NS + (path + args + lang).encode('utf-8')

@mod.route('/compute/')
def compute():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    depth = request.args.get('depth', None)
    sort = request.args.get('sort', 'desc')

    metric = request.args.get('metric', None) # what we're looking at
    show = request.args.get('show', '')
    shows = show.split(",")
    data = compute_stats(metric, shows, limit=limit, offset=offset, depth=depth, sort=sort)
    return jsonify(data)

@mod.route('/carousel/')
@view_cache.cached(key_prefix=make_cache_key)
def carousel():
    limit = int(request.args.get('limit', 10))
    offset = int(request.args.get('offset', 0))
    depth = request.args.get('depth', None)
    sort = request.args.get('sort', 'desc')
    profile = request.args.get('profile', None)

    metric = request.args.get('metric', None) # what we're looking at
    show = request.args.get('show', '')
    shows = show.split(",")

    data = stats_list(metric, shows, limit=limit, offset=offset, sort=sort, depth=depth, listify=True)
    items = get_profiles(data, profile)

    return json.dumps(items)
