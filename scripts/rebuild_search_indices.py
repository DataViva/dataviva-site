import datetime
import whoosh
import flask_whooshalchemy
import os
import sys
from shutil import rmtree


program_start = datetime.datetime.utcnow()

basedir = os.path.abspath(__file__).split('/scripts/')[0]
if basedir not in sys.path:
    sys.path.insert(0, basedir)

from dataviva import app
from config import WHOOSH_BASE
from dataviva.apps.blog.models import Post
from dataviva.apps.news.models import Publication


def log(message):
    logtime = datetime.datetime.utcnow()
    logdiff = logtime - program_start
    print("{0} (+{1:.3f}): {2}".format(logtime.strftime("%Y-%m-%d %H:%M:%S"),
                                       logdiff.total_seconds(),
                                       message))


def rebuild_index(model):
    log("Rebuilding {0} index...".format(model.__name__))
    primary_field = model.pure_whoosh.primary_key_name
    searchables = model.__searchable__
    index_writer = flask_whooshalchemy.whoosh_index(app, model)

    entries = model.query.all()

    entry_count = 0
    with index_writer.writer() as writer:
        for entry in entries:
            index_attrs = {}
            for field in searchables:
                index_attrs[field] = unicode(getattr(entry, field))

            index_attrs[primary_field] = unicode(getattr(entry, primary_field))
            writer.update_document(**index_attrs)
            entry_count += 1

    log("Rebuilt {0} {1} search index entries.".format(
        str(entry_count), model.__name__))


if __name__ == "__main__":
    if os.path.exists(WHOOSH_BASE):
        rmtree(WHOOSH_BASE)
    model_list = [Post, Publication]
    for model in model_list:
        rebuild_index(model)
