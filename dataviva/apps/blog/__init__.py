import flask_whooshalchemy as whooshalchemy
from dataviva import app
from models import Post


whooshalchemy.whoosh_index(app, Post)
