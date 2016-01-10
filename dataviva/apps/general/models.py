from datetime import datetime
from dataviva import db

import string, random

class Short(db.Model):

    __tablename__ = 'apps_short'

    slug = db.Column(db.String(30), unique=True, primary_key=True)
    long_url = db.Column(db.String(255), unique=True)
    created = db.Column(db.DateTime, default=datetime.now)
    clicks = db.Column(db.Integer, default=0)

    @staticmethod
    def make_unique_slug(long_url):

        # Helper to generate random URL string
        # Thx EJF: https://github.com/ericjohnf/urlshort
        def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
            return ''.join(random.choice(chars) for x in range(size))

        # test if it already exists
        short = Short.query.filter_by(long_url = long_url).first()
        if short:
            return short.slug
        else:
            while True:
                new_slug = id_generator()
                if Short.query.filter_by(slug = new_slug).first() == None:
                    break
            return new_slug

    def __repr__(self):
        return "<ShortURL: '%s'>" % self.long_url
