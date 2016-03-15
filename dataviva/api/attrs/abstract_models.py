from dataviva import db
from flask import g
from dataviva.utils.title_case import title_case


class BasicAttr(object):
    name_en = db.Column(db.String(200))
    name_pt = db.Column(db.String(200))
    color = db.Column(db.String(7))
    gender_pt = db.Column(db.String(1))
    plural_pt = db.Column(db.Boolean())
    article_pt = db.Column(db.Boolean())

    def name(self):
        lang = getattr(g, "locale", "en")
        return title_case(getattr(self, "name_"+lang))

    def preposition(self, prepositon):
        if self.article_pt:
            return 'no' if self.gender_pt == 'm' else 'na'
        return 'em'

    def article(self):
        return "a"


class ExpandedAttr(BasicAttr):
    desc_en = db.Column(db.Text())
    desc_pt = db.Column(db.Text())
    keywords_en = db.Column(db.String(100))
    keywords_pt = db.Column(db.String(100))
