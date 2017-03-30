import flask_whooshalchemy as whooshalchemy
from dataviva import app
from models import Publication


whooshalchemy.whoosh_index(app, Publication)
